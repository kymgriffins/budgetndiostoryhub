"""
URL configuration for Next.js static export integration.
"""
from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views


# Build explicit URL patterns for known pages
urlpatterns = [
    # Serve Next.js static assets from _next folder
    re_path(r'^_next/(?P<path_info>.*)$', views.serve_next_static, name='next_static'),
    
    # Serve root-level assets (favicon, images) from templates/out
    re_path(r'^(?P<filename>favicon\.ico)$', views.serve_next_asset, name='nextjs_favicon'),
    re_path(r'^(?P<filename>opengraph-image\.png)$', views.serve_next_asset, name='nextjs_og'),
    re_path(r'^(?P<filename>twitter-image\.png)$', views.serve_next_asset, name='nextjs_twitter'),
    re_path(r'^(?P<filename>logo\.svg)$', views.serve_next_asset, name='nextjs_logo'),
    re_path(r'^(?P<filename>bnsoo1\.mp4)$', views.serve_next_asset, name='nextjs_video'),
    
    # Serve root index.html
    path('', views.NextJSPageView.as_view(), {'path': ''}, name='nextjs_index'),
    
    # Explicit routes for known Next.js pages
    path('home/', views.NextJSPageView.as_view(), {'path': 'home'}, name='nextjs_home'),
    path('about/', views.NextJSPageView.as_view(), {'path': 'about'}, name='nextjs_about'),
    path('blog/', views.NextJSPageView.as_view(), {'path': 'blog'}, name='nextjs_blog'),
    path('contact/', views.NextJSPageView.as_view(), {'path': 'contact'}, name='nextjs_contact'),
    path('videos/', views.NextJSPageView.as_view(), {'path': 'videos'}, name='nextjs_videos'),
    path('donate/', views.NextJSPageView.as_view(), {'path': 'donate'}, name='nextjs_donate'),
    path('newsletter/', views.NextJSPageView.as_view(), {'path': 'newsletter'}, name='nextjs_newsletter'),
    path('subscribe/', views.NextJSPageView.as_view(), {'path': 'subscribe'}, name='nextjs_subscribe'),
    path('take-action/', views.NextJSPageView.as_view(), {'path': 'take-action'}, name='nextjs_take_action'),
    path('learn/', views.NextJSPageView.as_view(), {'path': 'learn'}, name='nextjs_learn'),
    path('insights/', views.NextJSPageView.as_view(), {'path': 'insights'}, name='nextjs_insights'),
    path('reports/', views.NextJSPageView.as_view(), {'path': 'reports'}, name='nextjs_reports'),
    path('tracker/', views.NextJSPageView.as_view(), {'path': 'tracker'}, name='nextjs_tracker'),
    path('media-hub/', views.NextJSPageView.as_view(), {'path': 'media-hub'}, name='nextjs_media_hub'),
    path('organization/', views.NextJSPageView.as_view(), {'path': 'organization'}, name='nextjs_organization'),
    path('partners/', views.NextJSPageView.as_view(), {'path': 'partners'}, name='nextjs_partners'),
    path('services/', views.NextJSPageView.as_view(), {'path': 'services'}, name='nextjs_services'),
    path('advertisements/', views.NextJSPageView.as_view(), {'path': 'advertisements'}, name='nextjs_advertisements'),
    path('news/', views.NextJSPageView.as_view(), {'path': 'news'}, name='nextjs_news'),
    path('design/', views.NextJSPageView.as_view(), {'path': 'design'}, name='nextjs_design'),
    path('loading-demo/', views.NextJSPageView.as_view(), {'path': 'loading-demo'}, name='nextjs_loading_demo'),
    path('testimonial-02/', views.NextJSPageView.as_view(), {'path': 'testimonial-02'}, name='nextjs_testimonial'),
    path('footer-01/', views.NextJSPageView.as_view(), {'path': 'footer-01'}, name='nextjs_footer'),
    path('hero-01/', views.NextJSPageView.as_view(), {'path': 'hero-01'}, name='nextjs_hero'),
    
    # Auth pages
    path('auth/', views.NextJSPageView.as_view(), {'path': 'auth'}, name='nextjs_auth'),
    
    # Dashboard
    path('dashboard/', views.NextJSPageView.as_view(), {'path': 'dashboard'}, name='nextjs_dashboard'),
    
    # Catch-all for other Next.js pages (dynamic routing)
    re_path(r'^(?P<path>.*)/$', views.NextJSPageView.as_view(), name='nextjs_page'),
]
