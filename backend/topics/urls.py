"""
论文题目URL配置
"""
from django.urls import path
from . import views

app_name = 'topics'

urlpatterns = [
    path('', views.TopicListView.as_view(), name='list'),
    path('<int:pk>/', views.TopicDetailView.as_view(), name='detail'),
    path('teacher/', views.TeacherTopicListView.as_view(), name='teacher_list'),
    path('create/', views.TopicCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.TopicEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.TopicDeleteView.as_view(), name='delete'),
]
