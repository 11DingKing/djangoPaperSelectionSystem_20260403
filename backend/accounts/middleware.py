"""
账户中间件
"""
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    """登录验证中间件"""
    
    EXEMPT_URLS = [
        '/accounts/login/',
        '/admin/',
        '/static/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            if not any(path.startswith(url) for url in self.EXEMPT_URLS):
                return redirect(f"{reverse('accounts:login')}?next={path}")
        
        return self.get_response(request)
