from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sentinel.views import (
    BlogOwnerViewSet, WorkExperienceViewSet, EducationViewSet, 
    SkillViewSet, ProjectsViewSet, BlogViewSet, EmailSubscriberViewSet, 
    ChatMessagesViewSet, VisitorsViewSet, SystemSettingsViewSet,
    BlogTagsViewSet, BlogTagMappingViewSet
)
from . import views

# 创建路由器并注册viewset
router = DefaultRouter()
router.register(r'owner', BlogOwnerViewSet)
router.register(r'work-experience', WorkExperienceViewSet)
router.register(r'education', EducationViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'projects', ProjectsViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'blog-tags', BlogTagsViewSet)
router.register(r'blog-tag-mapping', BlogTagMappingViewSet)
router.register(r'subscribe', EmailSubscriberViewSet)
router.register(r'chat-messages', ChatMessagesViewSet)
router.register(r'visitors', VisitorsViewSet)
router.register(r'settings', SystemSettingsViewSet)

# API URL配置
urlpatterns = [
    # 获取本周GitHub热门项目列表
    # 访问地址：/api/top10/
    # 请求方法：GET
    path('top10/', views.get_top10_projects),
    
    # 与智能代理对话
    # 访问地址：/api/chat/
    # 请求方法：POST
    path('chat/', views.chat_with_agent),
    
    # 获取欢迎消息
    # 访问地址：/api/welcome/
    # 请求方法：GET
    path('welcome/', views.get_welcome_message),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
