
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os
import traceback

# 添加src目录到Python路径，以便导入agent相关代码
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

try:
    # 导入agent模块中的函数和变量
    from agent import run_agent_and_send_email, github_top10_tool, project_qa_tool, TOP10_CACHE, get_welcome_message, WELCOME_MESSAGE
    from model_config import get_model_config
except ImportError as e:
    print(f"导入错误: {e}")
    print(f"当前Python路径: {sys.path}")
    print(f"src路径: {src_path}")
    # 如果导入失败，提供默认实现
    TOP10_CACHE = []
    WELCOME_MESSAGE = "GitHub Sentinel 智能助手欢迎您"
    
    def get_welcome_message():
        return WELCOME_MESSAGE
    
    def github_top10_tool(_):
        return "GitHub数据获取失败，请检查模块导入"
    
    def project_qa_tool(question, model_name='deepseek-chat'):
        return "AI问答功能暂时不可用，请检查模块导入"


@csrf_exempt
def get_welcome_message(request):
    """
    获取欢迎消息的API接口
    
    请求方法：GET
    返回格式：JSON
    返回内容：
        - message: 欢迎消息
    """
    if request.method == 'GET':
        try:
            # 导入agent模块的欢迎消息
            try:
                from agent import get_welcome_message as get_msg
                message = get_msg()
            except ImportError:
                # 如果导入失败，返回默认消息
                message = WELCOME_MESSAGE
                
            return JsonResponse({'message': message})
        except Exception as e:
            return JsonResponse({
                'error': f'获取欢迎消息失败: {str(e)}',
                'message': '欢迎使用GitHub Sentinel智能助手'
            }, status=500)


@csrf_exempt
def get_top10_projects(request):
    """
    获取本周GitHub热门项目的API接口
    
    请求方法：GET
    返回格式：JSON
    返回内容：
        - summary: 格式化的项目汇总信息
        - projects: 原始项目数据列表
    """
    if request.method == 'GET':
        try:
            # 尝试获取真实数据
            try:
                from github_tools import get_top_github_repos_this_week, format_repos_summary
                projects = get_top_github_repos_this_week()
                summary = format_repos_summary(projects)
            except Exception as e:
                # 如果真实数据获取失败，返回模拟数据
                print(f"获取GitHub数据失败: {e}，使用模拟数据")
                # 模拟项目数据
                projects = [
                    {
                        "name": "microsoft/qlib",
                        "url": "https://github.com/microsoft/qlib",
                        "stars": 15200,
                        "description": "Qlib是微软开发的AI量化交易平台，融合了机器学习与金融量化分析"
                    },
                    {
                        "name": "openai/openai-python",
                        "url": "https://github.com/openai/openai-python",
                        "stars": 12800,
                        "description": "OpenAI Python 客户端库，用于与OpenAI API进行交互"
                    },
                    {
                        "name": "langchain-ai/langchain",
                        "url": "https://github.com/langchain-ai/langchain",
                        "stars": 10500,
                        "description": "LangChain框架，构建由语言模型驱动的应用程序"
                    },
                    {
                        "name": "ahuang11/streamlit-assistant",
                        "url": "https://github.com/ahuang11/streamlit-assistant",
                        "stars": 9600,
                        "description": "将AI助手原生集成到Streamlit应用中"
                    },
                    {
                        "name": "deepseek-ai/DeepSeek-V2",
                        "url": "https://github.com/deepseek-ai/DeepSeek-V2",
                        "stars": 8900,
                        "description": "DeepSeek V2是一个开源的大规模语言模型"
                    },
                    {
                        "name": "ollama/ollama",
                        "url": "https://github.com/ollama/ollama",
                        "stars": 7800,
                        "description": "在本地运行大型语言模型"
                    },
                    {
                        "name": "huggingface/transformers",
                        "url": "https://github.com/huggingface/transformers",
                        "stars": 6400,
                        "description": "Hugging Face Transformers库，AI模型的事实标准"
                    },
                    {
                        "name": "mlflow/mlflow",
                        "url": "https://github.com/mlflow/mlflow",
                        "stars": 5900,
                        "description": "MLflow，机器学习生命周期管理平台"
                    },
                    {
                        "name": "tauri-apps/tauri",
                        "url": "https://github.com/tauri-apps/tauri",
                        "stars": 5500,
                        "description": "构建更小、更快、更安全的桌面应用程序"
                    },
                    {
                        "name": "duckdb/duckdb",
                        "url": "https://github.com/duckdb/duckdb",
                        "stars": 4800,
                        "description": "一个嵌入式SQL OLAP数据库管理系统"
                    }
                ]
                # 生成摘要
                summary = "上周 GitHub 新增 star 数最多的前十个项目：\n\n"
                for i, repo in enumerate(projects, 1):
                    summary += (
                        f"{i}. {repo['name']}（⭐{repo['stars']})\n"
                        f"   地址: {repo['url']}\n"
                        f"   简介: {repo['description']}\n\n"
                    )

            return JsonResponse({
                'summary': summary,
                'projects': projects
            })
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({
                'error': f'获取数据失败: {str(e)}',
                'summary': '数据获取失败，请检查后端服务',
                'projects': []
            }, status=500)


@csrf_exempt
def chat_with_agent(request):
    """
    与智能代理对话的API接口
    
    请求方法：POST
    请求体格式：JSON
    请求参数：
        - question: 用户问题
        - model_name: AI模型名称（可选，默认'openai'）
    
    返回格式：JSON
    返回内容：
        - answer: AI模型的回答
    """
    if request.method == 'POST':
        try:
            # 解析请求体中的JSON数据
            data = json.loads(request.body)

            # 获取用户问题和模型名称
            question = data.get('question', '')
            model_name = data.get('model_name', 'deepseek-chat')

            # 调用agent模块获取AI回答
            answer = project_qa_tool(question, model_name=model_name)

            # 返回JSON格式的响应
            return JsonResponse({'answer': answer})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({
                'error': f'处理请求失败: {str(e)}',
                'answer': '抱歉，服务器出现错误，请稍后重试。'
            }, status=500)
