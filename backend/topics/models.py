"""
论文题目模型
"""
from django.db import models
from accounts.models import User


class Topic(models.Model):
    """论文题目模型"""
    
    class Status(models.IntegerChoices):
        OPEN = 1, '开放选题'
        FULL = 2, '名额已满'
        CLOSED = 3, '已关闭'
    
    title = models.CharField('题目名称', max_length=200)
    description = models.TextField('题目描述')
    requirements = models.TextField('选题要求', blank=True)
    max_students = models.PositiveIntegerField('最大可选人数', default=1)
    current_count = models.PositiveIntegerField('当前已选人数', default=0)
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='topics',
        verbose_name='指导教师'
    )
    status = models.IntegerField('状态', choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'topic'
        verbose_name = '论文题目'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def available_slots(self):
        """剩余名额"""
        return max(0, self.max_students - self.current_count)
    
    @property
    def is_available(self):
        """是否可选"""
        return self.status == self.Status.OPEN and self.available_slots > 0
    
    def update_status(self):
        """更新状态"""
        if self.current_count >= self.max_students:
            self.status = self.Status.FULL
        elif self.status == self.Status.FULL and self.current_count < self.max_students:
            self.status = self.Status.OPEN
        self.save(update_fields=['status'])
    
    @property
    def current_students(self):
        """别名，兼容模板"""
        return self.current_count
