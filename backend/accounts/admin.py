"""
账户后台管理
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'real_name', 'role', 'email', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'real_name', 'email')
    ordering = ('-created_at',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('real_name', 'role', 'student_id', 'teacher_id', 'phone')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('扩展信息', {'fields': ('real_name', 'role', 'student_id', 'teacher_id', 'phone')}),
    )
