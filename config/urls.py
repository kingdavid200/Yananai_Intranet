"""
URL configuration for Project Yananai Intranet.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('directory/', include('directory.urls')),
    path('documents/', include('documents.urls')),
    path('news/', include('news.urls')),
    path('projects/', include('projects.urls')),
    path('', include('accounts.dashboard_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
