"""
用户模型定义
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型"""
    
    class Role(models.IntegerChoices):
        STUDENT = 1, '学生'
        TEACHER = 2, '教师'
        ADMIN = 3, '管理员'
    
    real_name = models.CharField('真实姓名', max_length=50)
    role = models.IntegerField('角色', choices=Role.choices, default=Role.STUDENT)
    student_id = models.CharField('学号', max_length=20, blank=True, null=True)
    teacher_id = models.CharField('工号', max_length=20, blank=True, null=True)
    phone = models.CharField('手机号', max_length=11, blank=True, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.real_name}({self.username})"
    
    @property
    def is_student(self):
        return self.role == self.Role.STUDENT
    
    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER
    
    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN
    
    @property
    def name(self):
        """别名，兼容模板"""
        return self.real_name
    
    @property
    def role_name(self):
        """角色名称字符串"""
        return {
            self.Role.STUDENT: 'student',
            self.Role.TEACHER: 'teacher',
            self.Role.ADMIN: 'admin',
        }.get(self.role, 'unknown')
