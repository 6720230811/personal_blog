#!/usr/bin/env python
"""
Django管理脚本
功能：Django的命令行工具，用于执行各种管理任务
"""
import os
import sys


def main():
    """
    主函数：运行Django管理任务
    """
    # 设置Django设置模块的默认值
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentinel.settings')
    
    try:
        # 导入Django管理命令执行器
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # 如果无法导入Django，提示用户检查安装
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # 执行Django管理命令
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
