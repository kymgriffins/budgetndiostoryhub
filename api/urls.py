"""api URL Configuration"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, FileResponse
from pathlib import Path
import mimetypes
from apps.core.views import api_docs
from apps.core import views_api


# Serve Next.js static files from templates/out/_next or public/_next
def serve_next_static(request, path_info):
    base_dir = Path(__file__).resolve().parent.parent
    
    # Check in templates/out/_next first (Next.js export)
    file_path = base_dir / 'templates' / 'out' / '_next' / path_info
    
    if not file_path.exists() or not file_path.is_file():
        # Fall back to public/_next
        file_path = base_dir / 'public' / '_next' / path_info
    
    if file_path.exists() and file_path.is_file():
        content_type, _ = mimetypes.guess_type(str(file_path))
        if content_type is None:
            content_type = 'application/octet-stream'
        
        response = FileResponse(open(file_path, 'rb'), content_type=content_type)
        # Cache static files for 1 year in production
        response['Cache-Control'] = 'public, max-age=31536000, immutable'
        return response
    
    return HttpResponse('Not Found', status=404)


# Serve other static files from public folder
def serve_public_file(request, filename):
    base_dir = Path(__file__).resolve().parent.parent
    
    # Check in public folder first
    file_path = base_dir / 'public' / filename
    
    if not file_path.exists() or not file_path.is_file():
        # Fall back to templates/out folder
        file_path = base_dir / 'templates' / 'out' / filename
    
    if file_path.exists() and file_path.is_file():
        content_type, _ = mimetypes.guess_type(str(file_path))
        if content_type is None:
            content_type = 'application/octet-stream'
        
        response = FileResponse(open(file_path, 'rb'), content_type=content_type)
        response['Cache-Control'] = 'public, max-age=31536000, immutable'
        return response
    
    return HttpResponse('Not Found', status=404)


urlpatterns = [
    # Admin - must come first to avoid conflicts
    path('admin/', admin.site.urls),
    
    # Core app - serves all pages and CRUD operations (must be BEFORE Next.js)
    path('', include('apps.core.urls')),
    
    # Next.js static files - serve from _next folder
    re_path(r'^_next/(?P<path_info>.*)$', serve_next_static, name='next_static'),
    
    # Next.js pages - include the Next.js URL patterns (after core urls)
    path('', include('apps.nextjs.urls')),
    
    # Static files from public folder
    re_path(r'^(?P<filename>favicon\.ico)$', serve_public_file, name='favicon'),
    re_path(r'^(?P<filename>opengraph-image\.png)$', serve_public_file, name='og_image'),
    re_path(r'^(?P<filename>twitter-image\.png)$', serve_public_file, name='twitter_image'),
    re_path(r'^(?P<filename>logo\.svg)$', serve_public_file, name='logo'),
    re_path(r'^(?P<filename>bnsoo1\.mp4)$', serve_public_file, name='video'),
    
    # API Documentation
    path('api/docs/', api_docs, name='api_docs'),
    
    # API Dashboard - Custom HTML Interface
    path('api/', views_api.APIDashboardView.as_view(), name='api_dashboard'),
    path('api/browser/', views_api.APIBrowserView.as_view(), name='api_browser'),
    path('api/v1/<str:app_name>/', views_api.APIEndpointProxyView.as_view(), name='api_endpoint'),
    
    # API endpoints (original DRF endpoints)
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/content/', include('apps.content.urls')),
    path('api/v1/newsletter/', include('apps.newsletter.urls')),
    path('api/v1/sponsors/', include('apps.sponsors.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/cms/', include('apps.cms.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
