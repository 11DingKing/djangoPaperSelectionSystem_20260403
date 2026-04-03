"""
选题记录模型
"""
from django.db import models
from accounts.models import User
from topics.models import Topic


class Selection(models.Model):
    """选题记录模型"""
    
    class Status(models.IntegerChoices):
        PENDING = 1, '待审批'
        APPROVED = 2, '已通过'
        REJECTED = 3, '已拒绝'
    
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='selections',
        verbose_name='学生'
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='selections',
        verbose_name='论文题目'
    )
    status = models.IntegerField('状态', choices=Status.choices, default=Status.PENDING)
    student_reason = models.TextField('申请理由', blank=True)
    teacher_comment = models.TextField('审批意见', blank=True)
    created_at = models.DateTimeField('申请时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'selection'
        verbose_name = '选题记录'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        unique_together = ['student', 'topic']
    
    def __str__(self):
        return f"{self.student.real_name} - {self.topic.title}"
    
    @property
    def status_class(self):
        """状态对应的CSS类"""
        return {
            self.Status.PENDING: 'warning',
            self.Status.APPROVED: 'success',
            self.Status.REJECTED: 'danger',
        }.get(self.status, 'secondary')
    
    @property
    def status_name(self):
        """状态名称字符串"""
        return {
            self.Status.PENDING: 'pending',
            self.Status.APPROVED: 'approved',
            self.Status.REJECTED: 'rejected',
        }.get(self.status, 'unknown')
    
    @property
    def reason(self):
        """别名，兼容模板"""
        return self.student_reason
    
    @property
    def reject_reason(self):
        """别名，兼容模板"""
        return self.teacher_comment
