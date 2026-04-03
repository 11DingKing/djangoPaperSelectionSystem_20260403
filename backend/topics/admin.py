"""
论文题目后台管理
"""
from django.contrib import admin
from .models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'max_students', 'current_count', 'status', 'created_at')
    list_filter = ('status', 'teacher')
    search_fields = ('title', 'description', 'teacher__real_name')
    ordering = ('-created_at',)
