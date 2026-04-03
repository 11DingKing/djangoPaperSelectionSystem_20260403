"""
URL configuration for thesis_selection project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('topics/', include('topics.urls')),
    path('selections/', include('selections.urls')),
    path('', RedirectView.as_view(url='/topics/', permanent=False)),
]
