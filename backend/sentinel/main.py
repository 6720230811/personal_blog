"""
GitHub Sentinel 主程序入口
功能：启动GitHub监控代理并发送邮件通知
"""

import os
import time
import schedule
from datetime import datetime
import argparse
from dotenv import load_dotenv
from agent import run_agent_and_send_email
from github_tools import get_top_github_repos_this_week, format_repos_summary
from email_utils import send_github_report


def send_weekly_report():
    """
    发送每周GitHub热门项目报告
    """
    print(f"[{datetime.now()}] 开始发送每周GitHub热门项目报告...")
    
    # 从环境变量获取邮件配置
    to_email = os.getenv("TO_EMAIL")      # 收件人邮箱
    
    # 获取GitHub热门项目
    repos = get_top_github_repos_this_week()
    summary = format_repos_summary(repos)
    
    # 构建邮件主题，包含日期
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    subject = f"{date_str} - GitHub热门项目每周汇总"
    
    # 发送邮件
    success = send_github_report(to_email, summary, include_html=True, subject=subject)
    
    if success:
        print(f"[{datetime.now()}] 每周报告发送成功！")
    else:
        print(f"[{datetime.now()}] 每周报告发送失败！")
    
    return success

def run_scheduler():
    """
    运行定时任务调度器
    """
    # 安排每周一早上8点运行
    schedule.every().monday.at("08:00").do(send_weekly_report)
    
    print("定时任务已启动，将在每周一早上8点发送GitHub热门项目报告...")
    print(f"[{datetime.now()}] 下次执行时间：{schedule.next_run()}")
    
    # 持续运行调度器
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

def run_once():
    """
    立即运行一次，发送报告
    """
    # 加载环境变量配置
    load_dotenv()
    
    # 从环境变量获取邮件配置
    to_email = os.getenv("TO_EMAIL")      # 收件人邮箱
    email_user = os.getenv("EMAIL_USER")  # 发件人邮箱
    email_pass = os.getenv("EMAIL_PASS")  # 邮箱密码
    
    # 启动代理并发送邮件
    run_agent_and_send_email(to_email, email_user, email_pass)

if __name__ == "__main__":
    # 加载环境变量配置
    load_dotenv()
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="GitHub Sentinel - GitHub项目监控工具")
    parser.add_argument('--schedule', action='store_true', help='启动定时任务，每周一早上8点发送报告')
    parser.add_argument('--send-now', action='store_true', help='立即发送一次报告')
    
    args = parser.parse_args()
    
    if args.schedule:
        run_scheduler()
    elif args.send_now:
        send_weekly_report()
    else:
        run_once()