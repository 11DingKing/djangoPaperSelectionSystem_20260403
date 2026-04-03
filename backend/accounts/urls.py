"""
账户URL配置
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    # 管理员功能
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/users/', views.AdminUserListView.as_view(), name='admin_user_list'),
    path('admin/users/create/', views.AdminUserCreateView.as_view(), name='admin_user_create'),
    path('admin/users/<int:pk>/edit/', views.AdminUserEditView.as_view(), name='admin_user_edit'),
    path('admin/users/<int:pk>/delete/', views.AdminUserDeleteView.as_view(), name='admin_user_delete'),
]
