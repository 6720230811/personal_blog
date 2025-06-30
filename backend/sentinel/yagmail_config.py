"""
Yagmail邮件配置模块
功能：配置邮件服务器参数和提供高级邮件发送功能
"""

import os
import yagmail
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class EmailConfig:
    """
    邮件配置类
    用于管理不同邮件服务商的配置参数
    """
    
    # 常用邮件服务商配置
    EMAIL_PROVIDERS = {
        'gmail': {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'use_tls': True,
            'use_ssl': False
        },
        'qq': {
            'smtp_server': 'smtp.qq.com',
            'smtp_port': 587,
            'use_tls': True,
            'use_ssl': False
        },
        '163': {
            'smtp_server': 'smtp.163.com',
            'smtp_port': 587,
            'use_tls': True,
            'use_ssl': False
        },
        'outlook': {
            'smtp_server': 'smtp-mail.outlook.com',
            'smtp_port': 587,
            'use_tls': True,
            'use_ssl': False
        },
        'yahoo': {
            'smtp_server': 'smtp.mail.yahoo.com',
            'smtp_port': 587,
            'use_tls': True,
            'use_ssl': False
        }
    }
    
    def __init__(self, provider: str = 'gmail'):
        """
        初始化邮件配置
        
        参数：
            provider (str): 邮件服务商名称，支持 'gmail', 'qq', '163', 'outlook', 'yahoo'
        """
        self.provider = provider.lower()
        if self.provider not in self.EMAIL_PROVIDERS:
            raise ValueError(f"不支持的邮件服务商: {provider}")
        
        self.config = self.EMAIL_PROVIDERS[self.provider]
    
    def get_smtp_config(self) -> Dict[str, Any]:
        """
        获取SMTP配置
        
        返回：
            dict: SMTP配置字典
        """
        return self.config.copy()

class YagmailManager:
    """
    Yagmail管理器
    提供高级邮件发送功能
    """
    
    def __init__(self, email: str, password: str, provider: str = 'gmail'):
        """
        初始化Yagmail管理器
        
        参数：
            email (str): 发件人邮箱地址
            password (str): 邮箱密码或应用专用密码
            provider (str): 邮件服务商
        """
        self.email = email
        self.password = password
        self.provider = provider
        self.config = EmailConfig(provider)
        self.yag = None
    
    def connect(self) -> bool:
        """
        连接到邮件服务器
        
        返回：
            bool: 连接是否成功
        """
        try:
            smtp_config = self.config.get_smtp_config()
            self.yag = yagmail.SMTP(
                user=self.email,
                password=self.password,
                host=smtp_config['smtp_server'],
                port=smtp_config['smtp_port'],
                smtp_starttls=smtp_config['use_tls'],
                smtp_ssl=smtp_config['use_ssl']
            )
            return True
        except Exception as e:
            print(f"邮件服务器连接失败: {e}")
            return False
    
    def send_simple_email(self, to_email: str, subject: str, content: str) -> bool:
        """
        发送简单文本邮件
        
        参数：
            to_email (str): 收件人邮箱
            subject (str): 邮件主题
            content (str): 邮件内容
        
        返回：
            bool: 发送是否成功
        """
        try:
            if not self.yag:
                if not self.connect():
                    return False
            
            self.yag.send(to=to_email, subject=subject, contents=content)
            print(f"邮件发送成功: {to_email}")
            return True
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return False
    
    def send_html_email(self, to_email: str, subject: str, html_content: str, 
                       text_content: Optional[str] = None) -> bool:
        """
        发送HTML格式邮件
        
        参数：
            to_email (str): 收件人邮箱
            subject (str): 邮件主题
            html_content (str): HTML格式的邮件内容
            text_content (str, optional): 纯文本格式的邮件内容（备用）
        
        返回：
            bool: 发送是否成功
        """
        try:
            if not self.yag:
                if not self.connect():
                    return False
            
            contents = [html_content]
            if text_content:
                contents.append(text_content)
            
            self.yag.send(to=to_email, subject=subject, contents=contents)
            print(f"HTML邮件发送成功: {to_email}")
            return True
        except Exception as e:
            print(f"HTML邮件发送失败: {e}")
            return False
    
    def send_email_with_attachments(self, to_email: str, subject: str, content: str, 
                                   attachments: List[str]) -> bool:
        """
        发送带附件的邮件
        
        参数：
            to_email (str): 收件人邮箱
            subject (str): 邮件主题
            content (str): 邮件内容
            attachments (List[str]): 附件文件路径列表
        
        返回：
            bool: 发送是否成功
        """
        try:
            if not self.yag:
                if not self.connect():
                    return False
            
            self.yag.send(to=to_email, subject=subject, contents=content, attachments=attachments)
            print(f"带附件邮件发送成功: {to_email}")
            return True
        except Exception as e:
            print(f"带附件邮件发送失败: {e}")
            return False
    
    def send_bulk_email(self, to_emails: List[str], subject: str, content: str) -> Dict[str, bool]:
        """
        批量发送邮件
        
        参数：
            to_emails (List[str]): 收件人邮箱列表
            subject (str): 邮件主题
            content (str): 邮件内容
        
        返回：
            Dict[str, bool]: 每个邮箱的发送结果
        """
        results = {}
        
        for email in to_emails:
            success = self.send_simple_email(email, subject, content)
            results[email] = success
        
        return results
    
    def close(self):
        """
        关闭邮件连接
        """
        if self.yag:
            self.yag.close()

def create_email_manager_from_env() -> YagmailManager:
    """
    从环境变量创建邮件管理器
    
    返回：
        YagmailManager: 邮件管理器实例
    """
    email = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')
    provider = os.getenv('EMAIL_PROVIDER', 'gmail')
    
    if not email or not password:
        raise ValueError("请在环境变量中设置 EMAIL_USER 和 EMAIL_PASS")
    
    return YagmailManager(email, password, provider)

def send_github_weekly_report(to_email: str, summary: str, 
                             include_html: bool = True,
                             custom_subject: str = None) -> bool:
    """
    发送GitHub周报邮件
    
    参数：
        to_email (str): 收件人邮箱
        summary (str): 项目汇总信息
        include_html (bool): 是否包含HTML格式
        custom_subject (str, optional): 自定义邮件主题，如果提供则使用此主题
    
    返回：
        bool: 发送是否成功
    """
    try:
        manager = create_email_manager_from_env()
        
        subject = custom_subject or "本周 GitHub 热门新项目汇总"
        
        if include_html:
            # 创建HTML格式的邮件内容
            html_content = f"""
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                    .header {{ background-color: #f8f9fa; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .repo-item {{ margin-bottom: 20px; padding: 15px; border: 1px solid #e9ecef; border-radius: 5px; }}
                    .repo-name {{ color: #0366d6; font-weight: bold; }}
                    .repo-stars {{ color: #586069; }}
                    .repo-url {{ color: #0366d6; text-decoration: none; }}
                    .repo-description {{ color: #24292e; margin-top: 10px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🚀 本周 GitHub 热门新项目汇总</h1>
                    <p>发现最新、最热门的开源项目</p>
                </div>
                <div class="content">
                    <pre style="white-space: pre-wrap; font-family: monospace;">{summary}</pre>
                </div>
                <div style="text-align: center; margin-top: 30px; color: #586069;">
                    <p>由 GitHub Sentinel 自动生成</p>
                </div>
            </body>
            </html>
            """
            
            return manager.send_html_email(to_email, subject, html_content, summary)
        else:
            return manager.send_simple_email(to_email, subject, summary)
    
    except Exception as e:
        print(f"发送GitHub周报失败: {e}")
        return False 