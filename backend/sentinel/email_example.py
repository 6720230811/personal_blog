"""
邮件使用示例
功能：展示如何使用yagmail_config.py的各种邮件发送功能
"""

import os
from dotenv import load_dotenv
from yagmail_config import YagmailManager, send_github_weekly_report
from email_utils import send_email, send_email_advanced, send_github_report, send_bulk_emails

# 加载环境变量
load_dotenv()

def example_basic_email():
    """
    基础邮件发送示例
    """
    print("=== 基础邮件发送示例 ===")
    
    # 从环境变量获取配置
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    to_email = os.getenv("TO_EMAIL")
    
    if not all([email_user, email_pass, to_email]):
        print("请在.env文件中设置EMAIL_USER、EMAIL_PASS和TO_EMAIL")
        return
    
    # 使用简单的send_email函数
    success = send_email(
        to_email=to_email,
        subject="测试邮件",
        content="这是一封测试邮件，来自GitHub Sentinel系统。",
        user=email_user,
        password=email_pass
    )
    
    if success:
        print("✅ 基础邮件发送成功")
    else:
        print("❌ 基础邮件发送失败")

def example_advanced_email():
    """
    高级邮件发送示例
    """
    print("\n=== 高级邮件发送示例 ===")
    
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    to_email = os.getenv("TO_EMAIL")
    
    if not all([email_user, email_pass, to_email]):
        print("请在.env文件中设置EMAIL_USER、EMAIL_PASS和TO_EMAIL")
        return
    
    # HTML格式邮件内容
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            .header { background-color: #f0f0f0; padding: 20px; text-align: center; }
            .content { padding: 20px; }
            .highlight { color: #007bff; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎉 GitHub Sentinel 系统通知</h1>
        </div>
        <div class="content">
            <p>您好！</p>
            <p>这是一封来自 <span class="highlight">GitHub Sentinel</span> 系统的HTML格式邮件。</p>
            <p>系统功能包括：</p>
            <ul>
                <li>📊 GitHub热门项目监控</li>
                <li>🤖 AI智能问答</li>
                <li>📧 自动邮件通知</li>
                <li>🌐 Web界面展示</li>
            </ul>
            <p>感谢使用我们的服务！</p>
        </div>
    </body>
    </html>
    """
    
    # 发送HTML邮件
    success = send_email_advanced(
        to_email=to_email,
        subject="GitHub Sentinel - HTML格式邮件",
        content="这是纯文本版本的内容",
        user=email_user,
        password=email_pass,
        provider='gmail',
        html_content=html_content
    )
    
    if success:
        print("✅ HTML邮件发送成功")
    else:
        print("❌ HTML邮件发送失败")

def example_github_report():
    """
    GitHub报告邮件示例
    """
    print("\n=== GitHub报告邮件示例 ===")
    
    to_email = os.getenv("TO_EMAIL")
    
    if not to_email:
        print("请在.env文件中设置TO_EMAIL")
        return
    
    # 模拟GitHub项目汇总信息
    summary = """本周 GitHub 新增 star 数最多的前十个项目：

1. microsoft/vscode（⭐1500)
   地址: https://github.com/microsoft/vscode
   简介: Visual Studio Code - 轻量级但功能强大的源代码编辑器

2. facebook/react（⭐1200)
   地址: https://github.com/facebook/react
   简介: React - 用于构建用户界面的JavaScript库

3. tensorflow/tensorflow（⭐1000)
   地址: https://github.com/tensorflow/tensorflow
   简介: TensorFlow - 端到端开源机器学习平台

4. openai/whisper（⭐800)
   地址: https://github.com/openai/whisper
   简介: Whisper - 通用语音识别模型

5. vercel/next.js（⭐700)
   地址: https://github.com/vercel/next.js
   简介: Next.js - React框架，用于生产环境

6. tailwindlabs/tailwindcss（⭐600)
   地址: https://github.com/tailwindlabs/tailwindcss
   简介: Tailwind CSS - 实用优先的CSS框架

7. vuejs/vue（⭐500)
   地址: https://github.com/vuejs/vue
   简介: Vue.js - 渐进式JavaScript框架

8. pytorch/pytorch（⭐450)
   地址: https://github.com/pytorch/pytorch
   简介: PyTorch - 深度学习框架

9. kubernetes/kubernetes（⭐400)
   地址: https://github.com/kubernetes/kubernetes
   简介: Kubernetes - 容器编排平台

10. docker/compose（⭐350)
    地址: https://github.com/docker/compose
    简介: Docker Compose - 多容器Docker应用程序工具"""
    
    # 发送GitHub报告邮件
    success = send_github_report(to_email, summary, include_html=True)
    
    if success:
        print("✅ GitHub报告邮件发送成功")
    else:
        print("❌ GitHub报告邮件发送失败")

def example_bulk_email():
    """
    批量邮件发送示例
    """
    print("\n=== 批量邮件发送示例 ===")
    
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    
    if not all([email_user, email_pass]):
        print("请在.env文件中设置EMAIL_USER和EMAIL_PASS")
        return
    
    # 收件人列表（示例邮箱，实际使用时请替换为真实邮箱）
    to_emails = [
        "user1@example.com",
        "user2@example.com", 
        "user3@example.com"
    ]
    
    # 批量发送邮件
    results = send_bulk_emails(
        to_emails=to_emails,
        subject="GitHub Sentinel - 批量通知",
        content="这是一封批量发送的测试邮件。",
        user=email_user,
        password=email_pass,
        provider='gmail'
    )
    
    # 显示发送结果
    print("批量邮件发送结果：")
    for email, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        print(f"  {email}: {status}")

def example_different_providers():
    """
    不同邮件服务商示例
    """
    print("\n=== 不同邮件服务商示例 ===")
    
    # 展示支持的邮件服务商
    providers = ['gmail', 'qq', '163', 'outlook', 'yahoo']
    
    print("支持的邮件服务商：")
    for provider in providers:
        print(f"  - {provider}")
    
    print("\n注意：使用不同服务商时，请确保：")
    print("1. 在.env文件中设置正确的EMAIL_USER和EMAIL_PASS")
    print("2. 对于Gmail，需要使用应用专用密码")
    print("3. 对于QQ邮箱，需要在设置中开启SMTP服务")
    print("4. 对于163邮箱，需要开启SMTP服务并获取授权码")

def main():
    """
    主函数：运行所有示例
    """
    print("🚀 GitHub Sentinel 邮件功能示例")
    print("=" * 50)
    
    # 检查环境变量
    if not os.path.exists('.env'):
        print("⚠️  未找到.env文件，请先创建并配置环境变量")
        print("示例.env文件内容：")
        print("EMAIL_USER=your-email@gmail.com")
        print("EMAIL_PASS=your-app-password")
        print("TO_EMAIL=recipient@example.com")
        print("EMAIL_PROVIDER=gmail")
        return
    
    # 运行示例
    try:
        example_basic_email()
        example_advanced_email()
        example_github_report()
        example_bulk_email()
        example_different_providers()
        
        print("\n" + "=" * 50)
        print("🎉 所有示例运行完成！")
        
    except Exception as e:
        print(f"\n❌ 运行示例时出现错误: {e}")
        print("请检查环境变量配置和网络连接")

if __name__ == "__main__":
    main() 