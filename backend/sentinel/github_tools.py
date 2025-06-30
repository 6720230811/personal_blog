"""
GitHub工具模块
功能：获取GitHub热门项目信息和格式化输出
"""

import requests
from datetime import datetime, timedelta
import pytz
import re
from langchain_openai.chat_models.base import ChatOpenAI

def get_top_github_repos_this_week(top_n=10):
    """
    获取上周（自然周，周一到周日）GitHub新增star数最多的项目
    
    参数：
        top_n (int): 返回的项目数量，默认10个
    
    返回：
        list: 包含项目信息的字典列表，每个字典包含：
            - name: 项目全名 (owner/repo)
            - url: 项目GitHub地址
            - stars: star数量
            - description: 项目描述
    """
    tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(tz)
    # 计算本周一0点
    this_monday = now - timedelta(days=now.weekday())
    this_monday = this_monday.replace(hour=0, minute=0, second=0, microsecond=0)
    # 上周一0点
    last_monday = this_monday - timedelta(days=7)
    # 上周日23:59:59
    last_sunday = this_monday - timedelta(seconds=1)
    # 转为ISO8601格式
    last_monday_str = last_monday.strftime('%Y-%m-%dT%H:%M:%SZ')
    last_sunday_str = last_sunday.strftime('%Y-%m-%dT%H:%M:%SZ')
    # 构建GitHub API请求URL
    url = (
        f"https://api.github.com/search/repositories"
        f"?q=created:{last_monday_str}..{last_sunday_str}"
        f"&sort=stars&order=desc&per_page={top_n}"
    )
    
    # 设置请求头，使用GitHub API v3
    headers = {"Accept": "application/vnd.github+json"}
    
    # 发送GET请求到GitHub API
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 如果请求失败则抛出异常
    
    # 解析响应数据
    items = response.json().get("items", [])
    result = []
    
    # 提取每个项目的关键信息
    for repo in items:
        result.append({
            "name": repo["full_name"],        # 项目全名
            "url": repo["html_url"],          # 项目URL
            "stars": repo["stargazers_count"], # star数量
            "description": repo["description"] # 项目描述
        })
    return result

def format_repos_summary(repos):
    """
    格式化项目信息为可读的文本格式
    
    参数：
        repos (list): 项目信息列表
    
    返回：
        str: 格式化后的项目汇总文本
    """
    summary = "上周 GitHub 新增 star 数最多的前十个项目：\n\n"
    
    # 遍历项目列表，格式化每个项目信息
    for i, repo in enumerate(repos, 1):
        summary += (
            f"{i}. {repo['name']}（⭐{repo['stars']})\n"  # 项目名称和star数
            f"   地址: {repo['url']}\n"                   # 项目地址
            f"   简介: {repo['description']}\n\n"         # 项目描述
        )
    
    return summary

def get_github_repo_tree(repo_url, branch='main'):
    """
    获取GitHub仓库的文件和目录结构（主分支或指定分支）
    参数：
        repo_url (str): 仓库主页URL，如 https://github.com/owner/repo
        branch (str): 分支名，默认'main'
    返回：
        list: 目录结构的列表，每项为{'path': 路径, 'type': 'tree'或'blob'}
    """
    m = re.match(r'https://github.com/([^/]+)/([^/]+)', repo_url)
    if not m:
        return "仓库URL格式不正确"
    owner, repo = m.group(1), m.group(2)
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    headers = {"Accept": "application/vnd.github+json"}
    resp = requests.get(api_url, headers=headers)
    if resp.status_code != 200:
        return f"获取目录结构失败: {resp.status_code} {resp.text}"
    tree = resp.json().get('tree', [])
    return [{'path': item['path'], 'type': item['type']} for item in tree]

def get_github_file_content(repo_url, file_path, branch='main'):
    """
    获取GitHub仓库中某个文件的内容
    参数：
        repo_url (str): 仓库主页URL，例如 https://github.com/owner/repo
        file_path (str): 仓库中的文件路径，例如 README.md 或 src/main.py
        branch (str): 分支名，默认 main
    返回：
        str: 文件的原始文本内容
    """
    m = re.match(r'https://github.com/([^/]+)/([^/]+)', repo_url)
    if not m:
        return "仓库URL格式不正确"
    owner, repo = m.group(1), m.group(2)
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"
    headers = {"Accept": "application/vnd.github+json"}
    resp = requests.get(api_url, headers=headers)
    if resp.status_code != 200:
        return f"获取文件内容失败: {resp.status_code} {resp.text}"
    content = resp.json().get('content', '')
    import base64
    try:
        return base64.b64decode(content).decode('utf-8')
    except Exception as e:
        return f"内容解码失败: {e}"
