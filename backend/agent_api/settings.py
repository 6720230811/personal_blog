"""
agent_api应用设置
功能：定义agent_api应用的配置参数
作者：GitHub Sentinel Team
版本：0.0.1
"""

from pathlib import Path
import os

# 安装的应用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST框架
    'corsheaders',  # CORS跨域
    'sentinel',  # 自定义应用
]

# 中间件
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS中间件，必须放在开头
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 网站URL
SITE_URL = os.getenv('SITE_URL', 'http://localhost:3000')

# CORS设置
CORS_ALLOW_ALL_ORIGINS = True  # 开发环境下允许所有源
CORS_ALLOW_CREDENTIALS = True
# 生产环境应该限制来源
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8080",
#     "http://127.0.0.1:8080",
# ]

# REST框架设置
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}