"""api URL Configuration"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, FileResponse
from pathlib import Path
import mimetypes
from apps.core.views import api_docs, home, config_page, index
from apps.core import views_api

# Serve Next.js static files from _next folder
def serve_next_static(request, path_info):
    base_dir = Path(__file__).resolve().parent.parent
    file_path = base_dir / 'templates' / 'out' / '_next' / path_info
    
    if file_path.exists() and file_path.is_file():
        content_type, _ = mimetypes.guess_type(str(file_path))
        if content_type is None:
            # Default to octet-stream for unknown types
            content_type = 'application/octet-stream'
        
        response = FileResponse(open(file_path, 'rb'), content_type=content_type)
        response['Cache-Control'] = 'public, max-age=31536000'
        return response
    
    # Try to find the file by looking for files with similar patterns
    chunks_dir = base_dir / 'templates' / 'out' / '_next' / 'static' / 'chunks'
    if chunks_dir.exists():
        # Try to find a matching file (for hash mismatches)
        for f in chunks_dir.glob('*.js'):
            # Extract just the filename without path
            return HttpResponse('Not Found - File not found', status=404)
    
    return HttpResponse('Not Found', status=404)

# Serve other static files from out folder
def serve_out_file(request, filename):
    base_dir = Path(__file__).resolve().parent.parent
    
    # Check in templates/out
    file_path = base_dir / 'templates' / 'out' / filename
    if file_path.exists() and file_path.is_file():
        content_type, _ = mimetypes.guess_type(str(file_path))
        if content_type is None:
            content_type = 'application/octet-stream'
        
        response = FileResponse(open(file_path, 'rb'), content_type=content_type)
        response['Cache-Control'] = 'public, max-age=31536000'
        return response
    return HttpResponse('Not Found', status=404)

urlpatterns = [
    # Admin - must come first to avoid conflicts
    path('admin/', admin.site.urls),
    
    # Next.js static files - serve from _next folder
    re_path(r'^_next/(?P<path_info>.*)$', serve_next_static, name='next_static'),
    
    # Static files from out folder
    re_path(r'^(?P<filename>favicon\.ico)
    
    # Core app - serves all pages and CRUD operations
    path('', include('apps.core.urls')),
    
    # Main pages - serve from templates/
    path('home/', home, name='home'),
    path('index/', index, name='index'),
    path('config/', config_page, name='config'),
    
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
, serve_out_file, name='favicon'),
    re_path(r'^(?P<filename>opengraph-image\.png)
    
    # Core app - serves all pages and CRUD operations
    path('', include('apps.core.urls')),
    
    # Main pages - serve from templates/
    path('home/', home, name='home'),
    path('index/', index, name='index'),
    path('config/', config_page, name='config'),
    
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
, serve_out_file, name='og_image'),
    re_path(r'^(?P<filename>twitter-image\.png)
    
    # Core app - serves all pages and CRUD operations
    path('', include('apps.core.urls')),
    
    # Main pages - serve from templates/
    path('home/', home, name='home'),
    path('index/', index, name='index'),
    path('config/', config_page, name='config'),
    
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
, serve_out_file, name='twitter_image'),
    re_path(r'^(?P<filename>logo\.svg)
    
    # Core app - serves all pages and CRUD operations
    path('', include('apps.core.urls')),
    
    # Main pages - serve from templates/
    path('home/', home, name='home'),
    path('index/', index, name='index'),
    path('config/', config_page, name='config'),
    
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
, serve_out_file, name='logo'),
    re_path(r'^(?P<filename>bnsoo1\.mp4)
    
    # Core app - serves all pages and CRUD operations
    path('', include('apps.core.urls')),
    
    # Main pages - serve from templates/
    path('home/', home, name='home'),
    path('index/', index, name='index'),
    path('config/', config_page, name='config'),
    
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
, serve_out_file, name='video'),
    re_path(r'^(?P<filename>testimonial-black\.svg)
    
    # Core app - serves all pages and CRUD operations
    path('', include('apps.core.urls')),
    
    # Main pages - serve from templates/
    path('home/', home, name='home'),
    path('index/', index, name='index'),
    path('config/', config_page, name='config'),
    
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
, serve_out_file, name='testimonial'),
    re_path(r'^(?P<filename>senmedia\.png)
    
    # Core app - serves all pages and CRUD operations
    path('', include('apps.core.urls')),
    
    # Main pages - serve from templates/
    path('home/', home, name='home'),
    path('index/', index, name='index'),
    path('config/', config_page, name='config'),
    
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
, serve_out_file, name='senmedia'),
    
    # Core app - serves all pages and CRUD operations
    path('', include('apps.core.urls')),
    
    # Main pages - serve from templates/
    path('home/', home, name='home'),
    path('index/', index, name='index'),
    path('config/', config_page, name='config'),
    
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
