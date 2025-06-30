"""
Django项目主URL配置
功能：定义项目的URL路由规则
作者：GitHub Sentinel Team
版本：0.0.1
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, BlogOwnerViewSet, SkillViewSet, EducationViewSet, WorkExperienceViewSet, ProjectsViewSet

# 根路径视图函数
@csrf_exempt
def api_info(request):
    """
    根路径API信息页面
    功能：显示API服务状态和可用端点
    """
    return JsonResponse({
        'service': 'GitHub Sentinel API',
        'version': '0.0.1',
        'status': 'running',
        'endpoints': {
            'admin': '/admin/',
            'api_top10': '/api/top10/',
            'api_chat': '/api/chat/',
        },
        'description': 'GitHub项目监控和智能分析API服务'
    })

# 创建一个路由器并注册我们的视图集
router = DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'owner', BlogOwnerViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'education', EducationViewSet)
router.register(r'work-experience', WorkExperienceViewSet)
router.register(r'projects', ProjectsViewSet)
# 可以在此处添加更多的视图集

# URL模式配置
urlpatterns = [
    # 根路径 - API信息页面
    path('', api_info, name='api_info'),
    
    # Django管理后台URL
    path('admin/', admin.site.urls),
    
    # API路由：业务模型相关（sentinel app）
    path('api/', include(router.urls)),

    # 额外API路由：通用功能（agent_api 应用）
    path('api/', include('agent_api.urls')),
] 