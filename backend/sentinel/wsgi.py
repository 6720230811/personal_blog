"""
WSGI配置文件
功能：为Django项目提供WSGI应用入口
作者：GitHub Sentinel Team
版本：0.0.1

WSGI (Web Server Gateway Interface) 是Python Web应用与Web服务器之间的标准接口
更多信息请参考：https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 设置Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentinel.settings')

# 获取WSGI应用实例
application = get_wsgi_application() 