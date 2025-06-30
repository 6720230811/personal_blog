"""
邮件工具模块
功能：发送邮件通知（使用yagmail_config.py的高级功能）
"""

from yagmail_config import YagmailManager, send_github_weekly_report, create_email_manager_from_env

def send_email(to_email, subject, content, user, password):
    """
    发送邮件函数（向后兼容的简单接口）
    
    参数：
        to_email (str): 收件人邮箱地址
        subject (str): 邮件主题
        content (str): 邮件内容
        user (str): 发件人邮箱地址
        password (str): 发件人邮箱密码或应用专用密码
    
    注意：
        - 建议使用邮箱的应用专用密码而不是登录密码
        - 支持Gmail、QQ邮箱、163邮箱等主流邮箱服务
    """
    try:
        # 创建邮件管理器
        manager = YagmailManager(user, password)
        
        # 发送邮件
        success = manager.send_simple_email(to_email, subject, content)
        
        # 关闭连接
        manager.close()
        
        return success
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False

def send_email_advanced(to_email, subject, content, user, password, 
                       provider='gmail', html_content=None, attachments=None):
    """
    高级邮件发送函数
    
    参数：
        to_email (str): 收件人邮箱地址
        subject (str): 邮件主题
        content (str): 邮件内容
        user (str): 发件人邮箱地址
        password (str): 发件人邮箱密码或应用专用密码
        provider (str): 邮件服务商 ('gmail', 'qq', '163', 'outlook', 'yahoo')
        html_content (str, optional): HTML格式的邮件内容
        attachments (list, optional): 附件文件路径列表
    
    返回：
        bool: 发送是否成功
    """
    try:
        # 创建邮件管理器
        manager = YagmailManager(user, password, provider)
        
        # 根据参数选择发送方式
        if html_content:
            success = manager.send_html_email(to_email, subject, html_content, content)
        elif attachments:
            success = manager.send_email_with_attachments(to_email, subject, content, attachments)
        else:
            success = manager.send_simple_email(to_email, subject, content)
        
        # 关闭连接
        manager.close()
        
        return success
    except Exception as e:
        print(f"高级邮件发送失败: {e}")
        return False

def send_github_report(to_email, summary, include_html=True, subject=None):
    """
    发送GitHub项目报告邮件
    
    参数：
        to_email (str): 收件人邮箱地址
        summary (str): 项目汇总信息
        include_html (bool): 是否包含HTML格式
        subject (str, optional): 自定义邮件主题，默认为None使用默认主题
    
    返回：
        bool: 发送是否成功
    """
    return send_github_weekly_report(to_email, summary, include_html, subject)

def send_bulk_emails(to_emails, subject, content, user, password, provider='gmail'):
    """
    批量发送邮件
    
    参数：
        to_emails (list): 收件人邮箱地址列表
        subject (str): 邮件主题
        content (str): 邮件内容
        user (str): 发件人邮箱地址
        password (str): 发件人邮箱密码或应用专用密码
        provider (str): 邮件服务商
    
    返回：
        dict: 每个邮箱的发送结果
    """
    try:
        # 创建邮件管理器
        manager = YagmailManager(user, password, provider)
        
        # 批量发送
        results = manager.send_bulk_email(to_emails, subject, content)
        
        # 关闭连接
        manager.close()
        
        return results
    except Exception as e:
        print(f"批量邮件发送失败: {e}")
        return {email: False for email in to_emails}

def send_blog_notification(subscribers, blog_title, blog_summary, blog_url, blog_cover=None):
    """
    向订阅者发送博客更新通知邮件
    
    参数：
        subscribers (list): 订阅者列表，每个元素需要有email属性
        blog_title (str): 博客标题
        blog_summary (str): 博客摘要
        blog_url (str): 博客链接
        blog_cover (str, optional): 博客封面图片URL
    
    返回：
        dict: 发送结果统计 {'success': 成功数, 'fail': 失败数, 'total': 总数}
    """
    import os
    from dotenv import load_dotenv
    
    # 加载环境变量
    load_dotenv()
    
    # 从环境变量获取邮件配置
    email_user = os.getenv('EMAIL_USER')
    email_pass = os.getenv('EMAIL_PASS')
    email_provider = os.getenv('EMAIL_PROVIDER', 'gmail')
    site_name = os.getenv('SITE_NAME', '个人博客')
    
    if not email_user or not email_pass:
        print("邮件配置不完整，无法发送博客通知")
        return {'success': 0, 'fail': len(subscribers), 'total': len(subscribers)}
    
    # 创建邮件管理器
    manager = YagmailManager(email_user, email_pass, email_provider)
    
    # 构建HTML邮件内容
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
        <h1 style="color: #333;">新博客发布: {blog_title}</h1>
        
        {f'<div style="margin: 20px 0;"><img src="{blog_cover}" alt="文章封面" style="max-width: 100%; border-radius: 5px;"></div>' if blog_cover else ''}
        
        <div style="margin: 20px 0; color: #555; line-height: 1.6;">
            {blog_summary}
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{blog_url}" style="display: inline-block; background-color: #3dd6d0; color: #fff; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">
                阅读全文
            </a>
        </div>
        
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #888; font-size: 12px;">
            <p>您收到此邮件是因为您订阅了 {site_name} 的博客更新通知。</p>
            <p>如果您不想再收到此类通知，请点击 <a href="{{unsubscribe_url}}" style="color: #555;">退订链接</a>。</p>
        </div>
    </div>
    """
    
    # 纯文本版本
    text_content = f"""
    新博客发布: {blog_title}
    
    {blog_summary}
    
    阅读全文: {blog_url}
    
    您收到此邮件是因为您订阅了 {site_name} 的博客更新通知。
    如果您不想再收到此类通知，请访问退订链接。
    """
    
    # 发送邮件并统计结果
    results = {'success': 0, 'fail': 0, 'total': len(subscribers)}
    subject = f"新博客: {blog_title}"
    
    for subscriber in subscribers:
        # 替换订阅者特定的退订链接
        unsubscribe_url = f"http://localhost:8000/api/subscribe/unsubscribe/?token={getattr(subscriber, 'unsubscribe_token', '')}"
        personalized_html = html_content.replace("{{unsubscribe_url}}", unsubscribe_url)
        
        try:
            success = manager.send_html_email(
                subscriber.email, 
                subject, 
                personalized_html,
                text_content
            )
            
            if success:
                results['success'] += 1
            else:
                results['fail'] += 1
        except Exception as e:
            print(f"向 {subscriber.email} 发送邮件失败: {e}")
            results['fail'] += 1
    
    # 关闭连接
    manager.close()
    
    return results
