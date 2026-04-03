"""
选题后台管理
"""
from django.contrib import admin
from .models import Selection


@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('student__real_name', 'topic__title')
    ordering = ('-created_at',)
