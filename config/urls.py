"""
config URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myblog.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('account/', include('account.urls')),
    
    # Service Worker
    path('sw.js', TemplateView.as_view(
        template_name='sw.js',
        content_type='application/javascript'
    ), name='sw.js'),
    
    # ریدایرکت برای لوگو
    path('logo.png', RedirectView.as_view(
        url=settings.STATIC_URL + 'images/favicon.ico',
        permanent=False
    )),
    
    path('account/login/logo.png', RedirectView.as_view(
        url=settings.STATIC_URL + 'images/favicon.ico',
        permanent=False
    )),
]

# سرو کردن فایل‌های استاتیک و مدیا فقط در حالت توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)