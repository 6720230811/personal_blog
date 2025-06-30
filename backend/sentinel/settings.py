"""
Django项目设置文件
功能：配置Django项目的各种设置参数
作者：GitHub Sentinel Team
版本：0.0.1
"""

import os
from pathlib import Path

# 构建项目路径：获取当前文件的父目录的父目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全警告：在生产环境中请保持密钥的秘密性！
SECRET_KEY = 'django-insecure-your-secret-key-here'

# 安全警告：在生产环境中不要启用调试模式！
DEBUG = True

# 允许的主机列表
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 应用定义
INSTALLED_APPS = [
    'django.contrib.admin',      # Django管理后台
    'django.contrib.auth',       # 认证系统
    'django.contrib.contenttypes', # 内容类型框架
    'django.contrib.sessions',   # 会话框架
    'django.contrib.messages',   # 消息框架
    'django.contrib.staticfiles', # 静态文件管理
    'rest_framework',            # Django REST Framework
    'sentinel',                  # 自定义博客应用
    'agent_api',                 # 自定义API应用
    'corsheaders',               # CORS跨域支持
]

# 中间件配置
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 必须放在最前面
    'django.middleware.security.SecurityMiddleware',      # 安全中间件
    'django.contrib.sessions.middleware.SessionMiddleware', # 会话中间件
    'django.middleware.common.CommonMiddleware',          # 通用中间件
    'django.middleware.csrf.CsrfViewMiddleware',          # CSRF保护
    'django.contrib.auth.middleware.AuthenticationMiddleware', # 认证中间件
    'django.contrib.messages.middleware.MessageMiddleware',    # 消息中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 点击劫持保护
]

# 根URL配置
ROOT_URLCONF = 'sentinel.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI应用配置
WSGI_APPLICATION = 'sentinel.wsgi.application'

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',    # 数据库引擎：MySQL
        'NAME': 'personal_blog',                 # 数据库名称
        'USER': 'root',                          # 数据库用户名
        'PASSWORD': '272636',                  # 数据库密码
        'HOST': 'localhost',                     # 数据库主机
        'PORT': '3306',                          # 数据库端口
        'OPTIONS': {
            'charset': 'utf8mb4',                # 字符集
            'use_unicode': True,                 # 使用Unicode
        },
    }
}

# 密码验证器
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国际化配置
LANGUAGE_CODE = 'zh-hans'        # 中文简体
TIME_ZONE = 'Asia/Shanghai'      # 上海时区
USE_I18N = True                  # 启用国际化
USE_TZ = True                    # 启用时区支持

# 静态文件配置
STATIC_URL = 'static/'

# 默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS设置（用于前端集成）
CORS_ALLOW_ALL_ORIGINS = True    # 允许所有来源（仅用于开发环境）
CORS_ALLOW_CREDENTIALS = True    # 允许携带凭证

# 允许的CORS请求头
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

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