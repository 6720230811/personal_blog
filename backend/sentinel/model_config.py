"""
AI模型配置模块
功能：管理不同AI模型的API配置和参数
"""

# model_config.py
# 用于配置不同大模型的 API Key 及相关参数
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# AI模型配置字典
MODEL_CONFIG = {
    'deepseek-chat': {
        'model': 'deepseek/deepseek-v3-base:free',
        'api_key': os.getenv('DEEPSEEK_API_KEY'),          # deepseek-chat密钥
        'endpoint': os.getenv('DEEPSEEK_ENDPOINT'),        # deepseek-chat端点
    },
    # 'deepseek-chat': {
    #     'model': 'deepseek/deepseek-v3-base:free',
    #     'api_key': os.getenv('DEEPSEEK_API_KEY'),
    #     'endpoint': os.getenv('DEEPSEEK_ENDPOINT'),
    # },
    # 'qwen': {
    #     'api_key': os.getenv('QWEN_API_KEY'),           # 通义千问API密钥
    # },
}


def get_model_config(model_name):
    print("DEBUG get_model_config called with:", model_name)
    """
    获取指定模型的配置信息
    
    参数：
        model_name (str): 模型名称，如'openai'、'azure'等
    
    返回：
        dict: 模型配置字典，包含API密钥、模型名称等信息
              如果模型不存在，返回空字典
    """
    return MODEL_CONFIG.get(model_name, {})
