"""
GitHub Sentinel 智能代理模块
功能：提供GitHub项目监控和智能问答服务
"""

from langchain.agents import initialize_agent, Tool
from langchain_openai.chat_models.base import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from github_tools import get_top_github_repos_this_week, format_repos_summary, get_github_repo_tree,get_github_file_content
from email_utils import send_email
from model_config import get_model_config
from dotenv import load_dotenv

load_dotenv()

# 全局缓存本周top10项目，避免重复请求
TOP10_CACHE = []

# 系统欢迎提示词（面向初学者）
WELCOME_MESSAGE = """
你好，我是 GitHub Sentinel 智能助手，专注于本周 GitHub 最受欢迎的新项目。

💡 你可以这样问我：
1️⃣ "这周 GitHub 上最火的项目是什么？"
2️⃣ "这个项目是干什么的？适合新手吗？"
3️⃣ "我想参与其中一个项目开发，推荐哪个？"
4️⃣ "请列出 https://github.com/xxx 的文件结构"
5️⃣ "我只懂 Python，有没有适合的项目？"
"""

def get_welcome_message():
    """获取欢迎信息，供前端页面初始化时调用"""
    return WELCOME_MESSAGE

def github_top10_tool(_):
    """
    获取本周GitHub热门项目的工具函数
    参数：_ (忽略参数，保持工具接口一致性)
    返回：格式化的项目汇总信息
    """
    global TOP10_CACHE
    TOP10_CACHE = get_top_github_repos_this_week()
    return format_repos_summary(TOP10_CACHE)


def project_qa_tool(question, model_name='deepseek-chat'):
    """
    针对本周top10项目，回答用户的相关问题
    参数：
        question (str): 用户问题
        model_name (str): 使用的AI模型名称
    返回：str
    """
    projects = get_top_github_repos_this_week()
    if not projects:
        return "未能获取本周GitHub热门项目，请稍后重试。"

    context = format_repos_summary(projects)
    config = get_model_config(model_name)

    llm = ChatOpenAI(
        model=config.get('model'),
        api_key=config.get('api_key'),
        base_url=config.get('endpoint')
    )

    prompt = (
        "你是一个GitHub项目专家，以下是本周GitHub新增star数最多的前十个项目：\n"
        f"{context}\n"
        f"请你仅根据这些项目信息，用中文简明扼要地回答用户的问题：{question}\n"
        "如果问题与你提供的项目无关，请直接回复\"未找到相关信息\"。"
    )

    try:
        response = llm.invoke(prompt)
        return str(response.content)
    except Exception as e:
        print("LLM调用异常：", e)
        return f"LLM调用异常：{e}"


def github_tree_tool(repo_url, branch='main'):
    """
    获取GitHub仓库的文件和目录结构
    参数：
        repo_url (str): 仓库主页URL
        branch (str): 分支名
    返回：目录结构文本
    """
    tree = get_github_repo_tree(repo_url, branch)
    if isinstance(tree, str):
        return tree
    lines = [f"{item['type']}: {item['path']}" for item in tree]
    return "\n".join(lines[:100])


# 定义可用工具
tools = [
    Tool(name="GitHubTop10", func=github_top10_tool, description="获取本周 GitHub 新增 star 数最多的前十个项目"),
    Tool(name="ProjectQA", func=project_qa_tool, description="根据本周top10项目，回答用户关于这些项目的任何问题"),
    Tool(name="GitHubRepoTree", func=github_tree_tool, description="获取指定GitHub仓库的文件和目录结构，输入仓库主页URL"),
    Tool(name="GitHubFileContent", func=get_github_file_content, description="获取指定GitHub仓库文件内容")
]


def run_agent_and_send_email(to_email, email_user, email_pass, model_name='deepseek-chat'):
    """
    启动代理，推送热门项目邮件，并开启对话
    """
    # 步骤1：发送邮件
    summary = github_top10_tool("")
    send_email(to_email, "本周 GitHub 热门新项目汇总", summary, email_user, email_pass)
    print("📨 邮件已发送！")

    # 步骤2：启动 Agent
    config = get_model_config(model_name)
    
    llm = ChatOpenAI(
        model=config.get('model'),
        api_key=config.get('api_key'),
        base_url=config.get('endpoint')
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True, memory=memory)

    # 欢迎提示
    print(WELCOME_MESSAGE)

    # 对话循环
    while True:
        user_input = input("你：")
        if user_input.strip() == "退出":
            print("👋 对话结束。")
            break
        response = agent.run(user_input)
        print("机器人：" + response)
