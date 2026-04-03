"""
选题URL配置
"""
from django.urls import path
from . import views

app_name = 'selections'

urlpatterns = [
    path('apply/<int:topic_id>/', views.SelectionApplyView.as_view(), name='apply'),
    path('my/', views.MySelectionListView.as_view(), name='my_list'),
    path('pending/', views.PendingSelectionListView.as_view(), name='pending_list'),
    path('<int:pk>/approve/', views.SelectionApproveView.as_view(), name='approve'),
    path('<int:pk>/reject/', views.SelectionRejectView.as_view(), name='reject'),
    path('<int:pk>/cancel/', views.SelectionCancelView.as_view(), name='cancel'),
]
