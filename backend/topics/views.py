"""
论文题目视图
"""
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Topic
from .forms import TopicForm
from selections.models import Selection

logger = logging.getLogger(__name__)


class TopicListView(View):
    """论文题目列表（学生浏览）"""
    template_name = 'topics/list.html'
    
    def get(self, request):
        queryset = Topic.objects.filter(status=Topic.Status.OPEN).select_related('teacher')
        
        # 搜索
        keyword = request.GET.get('keyword', '').strip()
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | 
                Q(description__icontains=keyword) |
                Q(teacher__real_name__icontains=keyword)
            )
        
        # 分页
        paginator = Paginator(queryset, 10)
        page = request.GET.get('page', 1)
        topics = paginator.get_page(page)
        
        # 获取当前用户已选的题目ID
        selected_topic_ids = []
        if request.user.is_student:
            selected_topic_ids = list(
                Selection.objects.filter(
                    student=request.user,
                    status__in=[Selection.Status.PENDING, Selection.Status.APPROVED]
                ).values_list('topic_id', flat=True)
            )
        
        context = {
            'topics': topics,
            'keyword': keyword,
            'selected_topic_ids': selected_topic_ids,
        }
        return render(request, self.template_name, context)


class TopicDetailView(View):
    """论文题目详情"""
    template_name = 'topics/detail.html'
    
    def get(self, request, pk):
        topic = get_object_or_404(Topic.objects.select_related('teacher'), pk=pk)
        
        # 检查当前用户是否已选此题目
        has_selected = False
        selection = None
        if request.user.is_student:
            selection = Selection.objects.filter(
                student=request.user,
                topic=topic
            ).first()
            has_selected = selection is not None
        
        context = {
            'topic': topic,
            'has_selected': has_selected,
            'selection': selection,
        }
        return render(request, self.template_name, context)


class TeacherTopicListView(View):
    """教师题目管理列表"""
    template_name = 'topics/teacher_list.html'
    
    def get(self, request):
        if not request.user.is_teacher:
            messages.error(request, '您没有权限访问此页面')
            return redirect('topics:list')
        
        topics = Topic.objects.filter(teacher=request.user).order_by('-created_at')
        
        context = {
            'topics': topics,
        }
        return render(request, self.template_name, context)


class TopicCreateView(View):
    """创建论文题目"""
    template_name = 'topics/form.html'
    
    def get(self, request):
        if not request.user.is_teacher:
            messages.error(request, '只有教师才能发布论文题目')
            return redirect('topics:list')
        
        form = TopicForm()
        return render(request, self.template_name, {'form': form, 'is_edit': False})
    
    def post(self, request):
        if not request.user.is_teacher:
            messages.error(request, '只有教师才能发布论文题目')
            return redirect('topics:list')
        
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.teacher = request.user
            topic.save()
            logger.info(f"教师 {request.user.username} 创建了论文题目: {topic.title}")
            messages.success(request, '论文题目发布成功！')
            return redirect('topics:teacher_list')
        
        return render(request, self.template_name, {'form': form, 'is_edit': False})


class TopicEditView(View):
    """编辑论文题目"""
    template_name = 'topics/form.html'
    
    def get(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk, teacher=request.user)
        form = TopicForm(instance=topic)
        return render(request, self.template_name, {'form': form, 'is_edit': True, 'topic': topic})
    
    def post(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk, teacher=request.user)
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            logger.info(f"教师 {request.user.username} 更新了论文题目: {topic.title}")
            messages.success(request, '论文题目更新成功！')
            return redirect('topics:teacher_list')
        
        return render(request, self.template_name, {'form': form, 'is_edit': True, 'topic': topic})


class TopicDeleteView(View):
    """删除论文题目"""
    
    def post(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk, teacher=request.user)
        
        # 检查是否有已通过的选题
        from selections.models import Selection
        approved_count = Selection.objects.filter(
            topic=topic,
            status=Selection.Status.APPROVED
        ).count()
        
        if approved_count > 0:
            messages.error(request, '该题目已有学生选题通过，无法删除')
            return redirect('topics:teacher_list')
        
        title = topic.title
        topic.delete()
        logger.info(f"教师 {request.user.username} 删除了论文题目: {title}")
        messages.success(request, '论文题目已删除')
        return redirect('topics:teacher_list')
