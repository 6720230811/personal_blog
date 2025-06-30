from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    BlogOwner, WorkExperience, Education, Achievement,
    Skill, Projects, ProjectTags, ProjectTagMapping,
    Blogs, BlogTags, BlogTagMapping, ChatMessages,
    Visitors, SystemSettings, EmailSubscriber
)
from .serializers import (
    BlogOwnerSerializer, WorkExperienceSerializer, EducationSerializer, AchievementSerializer,
    SkillSerializer, ProjectsSerializer, ProjectTagsSerializer, ProjectTagMappingSerializer,
    ProjectDetailSerializer, BlogsSerializer, BlogTagsSerializer, BlogTagMappingSerializer,
    BlogDetailSerializer, ChatMessagesSerializer, VisitorsSerializer, SystemSettingsSerializer,
    EmailSubscriberSerializer
)

class BlogOwnerViewSet(viewsets.ReadOnlyModelViewSet):
    """博客所有者相关的API视图集"""
    queryset = BlogOwner.objects.all()
    serializer_class = BlogOwnerSerializer

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """技能相关的API视图集"""
    queryset = Skill.objects.all().order_by('display_order')
    serializer_class = SkillSerializer

class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    """教育经历相关的API视图集"""
    queryset = Education.objects.all().order_by('display_order')
    serializer_class = EducationSerializer

class WorkExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    """工作经历相关的API视图集"""
    queryset = WorkExperience.objects.all().order_by('display_order')
    serializer_class = WorkExperienceSerializer

class ProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    """项目经历相关的API视图集"""
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer

class BlogViewSet(viewsets.ModelViewSet):
    """博客相关的API视图集"""
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer
    
    def get_serializer_class(self):
        """根据操作类型返回不同的序列化器"""
        if self.action == 'retrieve':
            return BlogDetailSerializer  # 获取单个详情时使用详情序列化器
        return self.serializer_class
    
    def perform_create(self, serializer):
        """创建博客文章"""
        # 保存博客
        blog = serializer.save()
        
        # 如果博客设置为已发布，则发送邮件通知
        if blog.published:
            self.send_blog_notifications(blog)
    
    def perform_update(self, serializer):
        """更新博客文章"""
        # 获取更新前的状态
        was_published = False
        if self.get_object().id:
            old_blog = Blogs.objects.get(id=self.get_object().id)
            was_published = old_blog.published
        
        # 保存更新
        blog = serializer.save()
        
        # 如果博客从未发布变为已发布，则发送邮件通知
        if blog.published and not was_published:
            self.send_blog_notifications(blog)
    
    def send_blog_notifications(self, blog):
        """向订阅者发送博客通知"""
        from src.email_utils import send_blog_notification
        from django.conf import settings
        
        # 获取所有活跃且已确认的订阅者
        active_subscribers = EmailSubscriber.objects.filter(is_active=True, confirmed=True)
        if not active_subscribers.exists():
            print("没有活跃的订阅者，不发送通知")
            return
        
        # 构建博客链接
        blog_url = f"{settings.SITE_URL}/blog/{blog.id}"
        
        # 发送通知
        results = send_blog_notification(
            active_subscribers,
            blog.title,
            blog.summary or blog.content[:200] + "...",
            blog_url,
            blog.cover_image
        )
        
        print(f"博客通知发送结果: 成功 {results['success']}，失败 {results['fail']}，总共 {results['total']}")
        
        # 更新订阅者的最后发送时间
        from django.utils import timezone
        now = timezone.now()
        active_subscribers.update(last_sent_at=now)
    
    def retrieve(self, request, *args, **kwargs):
        """获取单个博客文章详情，并增加浏览量"""
        instance = self.get_object()
        # 增加浏览量
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """获取最新博客文章"""
        latest_blogs = Blogs.objects.filter(published=True).order_by('-published_at')[:5]
        serializer = self.get_serializer(latest_blogs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """获取推荐博客文章"""
        featured_blogs = Blogs.objects.filter(published=True, featured=True).order_by('-published_at')[:3]
        serializer = self.get_serializer(featured_blogs, many=True)
        return Response(serializer.data)

class SystemSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    """系统设置相关的API视图集"""
    queryset = SystemSettings.objects.all()
    serializer_class = SystemSettingsSerializer
    
    @action(detail=False, methods=['get'])
    def by_key(self, request):
        """根据键名获取系统设置"""
        key = request.query_params.get('key', None)
        if not key:
            return Response({'error': '请提供key参数'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            setting = SystemSettings.objects.get(setting_key=key)
            serializer = self.get_serializer(setting)
            return Response(serializer.data)
        except SystemSettings.DoesNotExist:
            return Response({'error': '设置不存在'}, status=status.HTTP_404_NOT_FOUND)

class EmailSubscriberViewSet(viewsets.ModelViewSet):
    """邮件订阅相关的API视图集"""
    queryset = EmailSubscriber.objects.all()
    serializer_class = EmailSubscriberSerializer
    
    def create(self, request, *args, **kwargs):
        """处理新的订阅请求"""
        # 检查邮箱是否已存在
        email = request.data.get('email')
        if not email:
            return Response({'error': '邮箱地址不能为空'}, status=status.HTTP_400_BAD_REQUEST)
            
        existing = EmailSubscriber.objects.filter(email=email).first()
        if existing:
            if existing.is_active:
                return Response({'message': '该邮箱已经订阅'}, status=status.HTTP_200_OK)
            else:
                # 重新激活已存在但不活跃的订阅
                existing.is_active = True
                existing.save()
                return Response({'message': '订阅已重新激活'}, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # 发送确认邮件
        self.send_confirmation_email(serializer.instance)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['get'])
    def confirm(self, request):
        """确认订阅"""
        token = request.query_params.get('token', None)
        if not token:
            return Response({'error': '确认令牌不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            subscriber = EmailSubscriber.objects.get(confirmation_token=token, is_active=True)
            subscriber.confirmed = True
            subscriber.save()
            return Response({'message': '订阅已确认'}, status=status.HTTP_200_OK)
        except EmailSubscriber.DoesNotExist:
            return Response({'error': '无效的确认令牌'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def unsubscribe(self, request):
        """取消订阅"""
        token = request.query_params.get('token', None)
        if not token:
            return Response({'error': '退订令牌不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            subscriber = EmailSubscriber.objects.get(unsubscribe_token=token)
            subscriber.is_active = False
            subscriber.save()
            return Response({'message': '已成功退订'}, status=status.HTTP_200_OK)
        except EmailSubscriber.DoesNotExist:
            return Response({'error': '无效的退订令牌'}, status=status.HTTP_404_NOT_FOUND)
    
    def send_confirmation_email(self, subscriber):
        """发送确认订阅邮件"""
        from src.email_utils import send_email_advanced
        from django.conf import settings
        import os
        
        # 构建确认URL
        confirm_url = f"{settings.SITE_URL}/api/subscribe/confirm/?token={subscriber.confirmation_token}"
        
        # 邮件内容
        subject = "确认您的博客订阅"
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
            <h2 style="color: #333;">确认您的博客订阅</h2>
            <p>您好 {subscriber.name or '朋友'},</p>
            <p>感谢您订阅我的博客通讯！请点击下面的按钮确认您的订阅：</p>
            <div style="text-align: center; margin: 20px 0;">
                <a href="{confirm_url}" style="display: inline-block; background-color: #3dd6d0; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 4px;">确认订阅</a>
            </div>
            <p>如果您没有请求订阅，请忽略此邮件。</p>
            <p>谢谢！</p>
        </div>
        """
        
        # 从环境变量获取邮件配置
        email_user = os.getenv('EMAIL_USER')
        email_pass = os.getenv('EMAIL_PASS')
        email_provider = os.getenv('EMAIL_PROVIDER', 'gmail')
        
        if email_user and email_pass:
            send_email_advanced(
                subscriber.email,
                subject,
                "请点击邮件中的链接确认您的订阅",
                email_user,
                email_pass,
                provider=email_provider,
                html_content=html_content
            )
        else:
            print(f"邮件配置不完整，无法发送确认邮件到 {subscriber.email}")

class VisitorsViewSet(viewsets.ModelViewSet):
    """访客相关的API视图集"""
    queryset = Visitors.objects.all()
    serializer_class = VisitorsSerializer

class BlogTagsViewSet(viewsets.ReadOnlyModelViewSet):
    """博客标签相关的API视图集"""
    queryset = BlogTags.objects.all()
    serializer_class = BlogTagsSerializer

class BlogTagMappingViewSet(viewsets.ReadOnlyModelViewSet):
    """博客标签映射相关的API视图集"""
    queryset = BlogTagMapping.objects.all()
    serializer_class = BlogTagMappingSerializer

class ChatMessagesViewSet(viewsets.ModelViewSet):
    """聊天消息相关的API视图集"""
    queryset = ChatMessages.objects.all()
    serializer_class = ChatMessagesSerializer

# 其他视图集可以根据需求添加 