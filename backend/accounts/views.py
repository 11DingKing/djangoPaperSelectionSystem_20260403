"""
账户视图
"""
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator

from .forms import LoginForm, UserForm
from .models import User

logger = logging.getLogger(__name__)


class LoginView(View):
    """用户登录视图"""
    template_name = 'accounts/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('topics:list')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            logger.info(f"用户登录成功: {user.username}")
            messages.success(request, f'欢迎回来，{user.real_name}！')
            
            # 根据角色跳转
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            if user.is_admin_user:
                return redirect('accounts:admin_dashboard')
            if user.is_teacher:
                return redirect('topics:teacher_list')
            return redirect('topics:list')
        
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """用户登出视图"""
    
    def get(self, request):
        if request.user.is_authenticated:
            logger.info(f"用户登出: {request.user.username}")
        logout(request)
        messages.info(request, '您已成功退出登录')
        return redirect('accounts:login')


class ProfileView(View):
    """个人信息视图"""
    template_name = 'accounts/profile.html'
    
    def get(self, request):
        context = {}
        user = request.user
        
        if user.is_teacher:
            from topics.models import Topic
            from selections.models import Selection
            context['topic_count'] = Topic.objects.filter(teacher=user).count()
            context['pending_count'] = Selection.objects.filter(
                topic__teacher=user, 
                status=Selection.Status.PENDING
            ).count()
        elif user.is_student:
            from selections.models import Selection
            context['selection_count'] = Selection.objects.filter(student=user).count()
            context['approved_count'] = Selection.objects.filter(
                student=user, 
                status=Selection.Status.APPROVED
            ).count()
        elif user.is_admin_user:
            from topics.models import Topic
            from selections.models import Selection
            context['user_count'] = User.objects.exclude(role=User.Role.ADMIN).count()
            context['topic_count'] = Topic.objects.count()
        
        return render(request, self.template_name, context)


class AdminDashboardView(View):
    """管理员仪表盘"""
    template_name = 'accounts/admin/dashboard.html'
    
    def get(self, request):
        if not request.user.is_admin_user:
            messages.error(request, '您没有权限访问此页面')
            return redirect('topics:list')
        
        from topics.models import Topic
        from selections.models import Selection
        
        context = {
            'teacher_count': User.objects.filter(role=User.Role.TEACHER).count(),
            'student_count': User.objects.filter(role=User.Role.STUDENT).count(),
            'topic_count': Topic.objects.count(),
            'selection_count': Selection.objects.count(),
            'pending_count': Selection.objects.filter(status=Selection.Status.PENDING).count(),
            'approved_count': Selection.objects.filter(status=Selection.Status.APPROVED).count(),
        }
        return render(request, self.template_name, context)


class AdminUserListView(View):
    """用户管理列表"""
    template_name = 'accounts/admin/user_list.html'
    
    def get(self, request):
        if not request.user.is_admin_user:
            messages.error(request, '您没有权限访问此页面')
            return redirect('topics:list')
        
        role_filter = request.GET.get('role', '')
        queryset = User.objects.exclude(role=User.Role.ADMIN).order_by('-created_at')
        
        if role_filter == 'teacher':
            queryset = queryset.filter(role=User.Role.TEACHER)
        elif role_filter == 'student':
            queryset = queryset.filter(role=User.Role.STUDENT)
        
        paginator = Paginator(queryset, 15)
        page = request.GET.get('page', 1)
        users = paginator.get_page(page)
        
        context = {
            'users': users,
            'role_filter': role_filter,
        }
        return render(request, self.template_name, context)


class AdminUserCreateView(View):
    """创建用户"""
    template_name = 'accounts/admin/user_form.html'
    
    def get(self, request):
        if not request.user.is_admin_user:
            messages.error(request, '您没有权限访问此页面')
            return redirect('topics:list')
        
        form = UserForm()
        return render(request, self.template_name, {'form': form, 'is_edit': False})
    
    def post(self, request):
        if not request.user.is_admin_user:
            messages.error(request, '您没有权限访问此页面')
            return redirect('topics:list')
        
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            logger.info(f"管理员创建了用户: {user.username}")
            messages.success(request, f'用户 {user.real_name} 创建成功')
            return redirect('accounts:admin_user_list')
        
        return render(request, self.template_name, {'form': form, 'is_edit': False})


class AdminUserEditView(View):
    """编辑用户"""
    template_name = 'accounts/admin/user_form.html'
    
    def get(self, request, pk):
        if not request.user.is_admin_user:
            messages.error(request, '您没有权限访问此页面')
            return redirect('topics:list')
        
        user = get_object_or_404(User, pk=pk)
        form = UserForm(instance=user)
        return render(request, self.template_name, {'form': form, 'is_edit': True, 'edit_user': user})
    
    def post(self, request, pk):
        if not request.user.is_admin_user:
            messages.error(request, '您没有权限访问此页面')
            return redirect('topics:list')
        
        user = get_object_or_404(User, pk=pk)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            logger.info(f"管理员更新了用户: {user.username}")
            messages.success(request, f'用户 {user.real_name} 更新成功')
            return redirect('accounts:admin_user_list')
        
        return render(request, self.template_name, {'form': form, 'is_edit': True, 'edit_user': user})


class AdminUserDeleteView(View):
    """删除用户"""
    
    def post(self, request, pk):
        if not request.user.is_admin_user:
            messages.error(request, '您没有权限访问此页面')
            return redirect('topics:list')
        
        user = get_object_or_404(User, pk=pk)
        if user.is_admin_user:
            messages.error(request, '不能删除管理员账号')
            return redirect('accounts:admin_user_list')
        
        username = user.username
        user.delete()
        logger.info(f"管理员删除了用户: {username}")
        messages.success(request, '用户已删除')
        return redirect('accounts:admin_user_list')
