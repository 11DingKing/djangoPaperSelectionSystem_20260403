"""
选题视图
"""
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.db import transaction

from .models import Selection
from .forms import SelectionApplyForm, SelectionReviewForm
from topics.models import Topic

logger = logging.getLogger(__name__)


class SelectionApplyView(View):
    """学生申请选题"""
    template_name = 'selections/apply.html'
    
    def get(self, request, topic_id):
        if not request.user.is_student:
            messages.error(request, '只有学生才能申请选题')
            return redirect('topics:list')
        
        topic = get_object_or_404(Topic.objects.select_related('teacher'), pk=topic_id)
        
        # 检查是否已申请
        existing = Selection.objects.filter(student=request.user, topic=topic).first()
        if existing:
            messages.warning(request, '您已经申请过此题目')
            return redirect('selections:my_list')
        
        # 检查是否已有通过的选题
        approved = Selection.objects.filter(
            student=request.user, 
            status=Selection.Status.APPROVED
        ).first()
        if approved:
            messages.warning(request, f'您已经有通过的选题：{approved.topic.title}')
            return redirect('selections:my_list')
        
        # 检查题目是否可选
        if not topic.is_available:
            messages.error(request, '该题目暂不可选')
            return redirect('topics:list')
        
        form = SelectionApplyForm()
        return render(request, self.template_name, {'form': form, 'topic': topic})
    
    @transaction.atomic
    def post(self, request, topic_id):
        if not request.user.is_student:
            messages.error(request, '只有学生才能申请选题')
            return redirect('topics:list')
        
        topic = get_object_or_404(Topic.objects.select_related('teacher'), pk=topic_id)
        form = SelectionApplyForm(request.POST)
        
        if form.is_valid():
            # 检查是否已申请
            existing = Selection.objects.filter(student=request.user, topic=topic).first()
            if existing:
                messages.warning(request, '您已经申请过此题目')
                return redirect('selections:my_list')
            
            # 检查是否已有通过的选题
            approved = Selection.objects.filter(
                student=request.user, 
                status=Selection.Status.APPROVED
            ).first()
            if approved:
                messages.warning(request, f'您已经有通过的选题：{approved.topic.title}')
                return redirect('selections:my_list')
            
            # 检查名额是否已满（包括待审批的申请）
            if not topic.is_available:
                messages.error(request, '该题目名额已满，无法申请')
                return redirect('topics:list')
            
            Selection.objects.create(
                student=request.user,
                topic=topic,
                student_reason=form.cleaned_data['reason']
            )
            logger.info(f"学生 {request.user.username} 申请了论文题目: {topic.title}")
            messages.success(request, '选题申请已提交，请等待教师审批')
            return redirect('selections:my_list')
        
        return render(request, self.template_name, {'form': form, 'topic': topic})


class MySelectionListView(View):
    """我的选题记录（学生）"""
    template_name = 'selections/my_list.html'
    
    def get(self, request):
        if not request.user.is_student:
            messages.error(request, '此页面仅供学生访问')
            return redirect('topics:list')
        
        selections = Selection.objects.filter(
            student=request.user
        ).select_related('topic', 'topic__teacher').order_by('-created_at')
        
        return render(request, self.template_name, {'selections': selections})


class PendingSelectionListView(View):
    """待审批列表（教师）"""
    template_name = 'selections/pending_list.html'
    
    def get(self, request):
        if not request.user.is_teacher:
            messages.error(request, '此页面仅供教师访问')
            return redirect('topics:list')
        
        # 获取该教师所有题目的选题申请
        selections = Selection.objects.filter(
            topic__teacher=request.user
        ).select_related('student', 'topic').order_by('status', '-created_at')
        
        pending_count = selections.filter(status=Selection.Status.PENDING).count()
        
        return render(request, self.template_name, {
            'selections': selections,
            'pending_count': pending_count,
        })


class SelectionApproveView(View):
    """通过选题申请"""
    
    @transaction.atomic
    def post(self, request, pk):
        if not request.user.is_teacher:
            messages.error(request, '只有教师才能审批选题')
            return redirect('topics:list')
        
        selection = get_object_or_404(
            Selection.objects.select_related('topic'),
            pk=pk,
            topic__teacher=request.user,
            status=Selection.Status.PENDING
        )
        
        form = SelectionReviewForm(request.POST)
        if form.is_valid():
            # 检查名额（包括待审批的申请）
            topic = selection.topic
            if topic.total_occupied > topic.max_students:
                messages.error(request, '该题目名额已满')
                return redirect('selections:pending_list')
            
            # 更新选题状态
            selection.status = Selection.Status.APPROVED
            selection.teacher_comment = form.cleaned_data.get('comment', '')
            selection.save()
            
            # 更新题目已选人数
            topic.current_count += 1
            topic.save(update_fields=['current_count'])
            topic.update_status()
            
            # 拒绝该学生的其他待审批申请，并更新对应题目的状态
            other_selections = Selection.objects.filter(
                student=selection.student,
                status=Selection.Status.PENDING
            ).exclude(pk=pk).select_related('topic')
            
            for sel in other_selections:
                sel.status = Selection.Status.REJECTED
                sel.teacher_comment = '学生已选择其他题目'
                sel.save()
                sel.topic.update_status()
            
            logger.info(f"教师 {request.user.username} 通过了学生 {selection.student.username} 的选题申请")
            messages.success(request, f'已通过 {selection.student.real_name} 的选题申请')
        
        return redirect('selections:pending_list')


class SelectionRejectView(View):
    """拒绝选题申请"""
    
    def post(self, request, pk):
        if not request.user.is_teacher:
            messages.error(request, '只有教师才能审批选题')
            return redirect('topics:list')
        
        selection = get_object_or_404(
            Selection,
            pk=pk,
            topic__teacher=request.user,
            status=Selection.Status.PENDING
        )
        
        form = SelectionReviewForm(request.POST)
        if form.is_valid():
            selection.status = Selection.Status.REJECTED
            selection.teacher_comment = form.cleaned_data.get('comment', '')
            selection.save()
            
            selection.topic.update_status()
            
            logger.info(f"教师 {request.user.username} 拒绝了学生 {selection.student.username} 的选题申请")
            messages.success(request, f'已拒绝 {selection.student.real_name} 的选题申请')
        
        return redirect('selections:pending_list')


class SelectionCancelView(View):
    """学生取消选题申请"""
    
    def post(self, request, pk):
        if not request.user.is_student:
            messages.error(request, '只有学生才能取消申请')
            return redirect('topics:list')
        
        selection = get_object_or_404(
            Selection,
            pk=pk,
            student=request.user,
            status=Selection.Status.PENDING
        )
        
        topic = selection.topic
        selection.delete()
        
        topic.update_status()
        
        logger.info(f"学生 {request.user.username} 取消了选题申请")
        messages.success(request, '已取消选题申请')
        
        return redirect('selections:my_list')
