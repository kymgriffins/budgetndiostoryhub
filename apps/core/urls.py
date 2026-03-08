from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views_crud
from . import views
from . import views_profile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
import json
import re

# CSRF token view - Enhanced with proper CORS headers
def csrf_token_view(request):
    """Get CSRF token for authenticated requests"""
    from django.middleware.csrf import get_token
    token = get_token(request)
    response = JsonResponse({'csrfToken': token})
    response['Access-Control-Allow-Origin'] = '*'
    return response

# Login view - SECURED with proper CSRF protection
def api_login_view(request):
    """Secure login endpoint with CSRF protection"""
    if request.method == 'POST':
        # Get CSRF token from header
        csrf_token = request.headers.get('X-CSRFToken')
        if not csrf_token:
            return JsonResponse({'error': 'CSRF token required'}, status=403)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({
                    'success': True, 
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'is_staff': user.is_staff,
                    },
                    'message': 'Login successful'
                })
            else:
                return JsonResponse({'error': 'Account is disabled'}, status=403)
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    elif request.method == 'OPTIONS':
        # Handle CORS preflight
        response = JsonResponse({})
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, X-CSRFToken'
        return response
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Logout view - Enhanced with CSRF protection
def api_logout_view(request):
    """Secure logout endpoint"""
    if request.method == 'POST':
        csrf_token = request.headers.get('X-CSRFToken')
        if not csrf_token:
            return JsonResponse({'error': 'CSRF token required'}, status=403)
        
        logout(request)
        return JsonResponse({'success': True, 'message': 'Logged out successfully'})
    elif request.method == 'OPTIONS':
        response = JsonResponse({})
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, X-CSRFToken'
        return response
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Current user view - Enhanced with more user data
def current_user_view(request):
    """Get current authenticated user"""
    if request.user.is_authenticated:
        return JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
            'date_joined': request.user.date_joined.isoformat() if request.user.date_joined else None,
        })
    return JsonResponse({'error': 'Not authenticated', 'authenticated': False}, status=401)

urlpatterns = [
    # CSRF and Auth API
    path('api/csrf/', csrf_token_view, name='csrf_token'),
    path('api/auth/login/', api_login_view, name='api_login'),
    path('api/auth/logout/', api_logout_view, name='api_logout'),
    path('api/auth/user/', current_user_view, name='current_user'),
    
    # Django Auth URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login_direct'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_direct'),
    path('accounts/register/', views.register_page, name='register'),
    path('register/', views.register_page, name='register_direct'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset_direct'),
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset.html'), name='password_reset_done'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    
    # Dashboard
    path('dashboard/', views_crud.dashboard, name='dashboard'),
    
    # Accounts URLs
    path('dashboard/users/', views_crud.AccountsListView.as_view(), {'model': 'users'}, name='user-list'),
    path('dashboard/donors/', views_crud.AccountsListView.as_view(), {'model': 'donors'}, name='donor-list'),
    path('dashboard/sponsors/', views_crud.AccountsListView.as_view(), {'model': 'sponsors'}, name='sponsor-list'),
    path('dashboard/partners/', views_crud.AccountsListView.as_view(), {'model': 'partners'}, name='partner-list'),
    
    # Content - Categories
    path('dashboard/categories/', views_crud.CategoryListView.as_view(), name='category-list'),
    path('dashboard/categories/create/', views_crud.CategoryCreateView.as_view(), name='category-create'),
    path('dashboard/categories/<int:pk>/edit/', views_crud.CategoryUpdateView.as_view(), name='category-update'),
    path('dashboard/categories/<int:pk>/delete/', views_crud.CategoryDeleteView.as_view(), name='category-delete'),
    
    # Content - Videos
    path('dashboard/videos/', views_crud.VideoListView.as_view(), name='video-list'),
    path('dashboard/videos/create/', views_crud.VideoCreateView.as_view(), name='video-create'),
    path('dashboard/videos/<int:pk>/edit/', views_crud.VideoUpdateView.as_view(), name='video-update'),
    path('dashboard/videos/<int:pk>/delete/', views_crud.VideoDeleteView.as_view(), name='video-delete'),
    
    # Content - Playlists
    path('dashboard/playlists/', views_crud.PlaylistListView.as_view(), name='playlist-list'),
    path('dashboard/playlists/create/', views_crud.PlaylistCreateView.as_view(), name='playlist-create'),
    path('dashboard/playlists/<int:pk>/edit/', views_crud.PlaylistUpdateView.as_view(), name='playlist-update'),
    path('dashboard/playlists/<int:pk>/delete/', views_crud.PlaylistDeleteView.as_view(), name='playlist-delete'),
    
    # Content - Blog Posts
    path('dashboard/posts/', views_crud.BlogPostListView.as_view(), name='blogpost-list'),
    path('dashboard/posts/create/', views_crud.BlogPostCreateView.as_view(), name='blogpost-create'),
    path('dashboard/posts/<int:pk>/edit/', views_crud.BlogPostUpdateView.as_view(), name='blogpost-update'),
    path('dashboard/posts/<int:pk>/delete/', views_crud.BlogPostDeleteView.as_view(), name='blogpost-delete'),
    
    # Content - News
    path('dashboard/news/', views_crud.NewsItemListView.as_view(), name='newsitem-list'),
    path('dashboard/news/create/', views_crud.NewsItemCreateView.as_view(), name='newsitem-create'),
    path('dashboard/news/<int:pk>/edit/', views_crud.NewsItemUpdateView.as_view(), name='newsitem-update'),
    path('dashboard/news/<int:pk>/delete/', views_crud.NewsItemDeleteView.as_view(), name='newsitem-delete'),
    
    # Newsletter - Subscribers
    path('dashboard/subscribers/', views_crud.SubscriberListView.as_view(), name='subscriber-list'),
    path('dashboard/subscribers/create/', views_crud.SubscriberCreateView.as_view(), name='subscriber-create'),
    path('dashboard/subscribers/<int:pk>/edit/', views_crud.SubscriberUpdateView.as_view(), name='subscriber-update'),
    path('dashboard/subscribers/<int:pk>/delete/', views_crud.SubscriberDeleteView.as_view(), name='subscriber-delete'),
    
    # Newsletter - Campaigns
    path('dashboard/campaigns/', views_crud.NewsletterCampaignListView.as_view(), name='campaign-list'),
    path('dashboard/campaigns/create/', views_crud.NewsletterCampaignCreateView.as_view(), name='campaign-create'),
    path('dashboard/campaigns/<int:pk>/edit/', views_crud.NewsletterCampaignUpdateView.as_view(), name='campaign-update'),
    path('dashboard/campaigns/<int:pk>/delete/', views_crud.NewsletterCampaignDeleteView.as_view(), name='campaign-delete'),
    
    # Sponsors - Donations
    path('dashboard/donations/', views_crud.DonationListView.as_view(), name='donation-list'),
    path('dashboard/donations/create/', views_crud.DonationCreateView.as_view(), name='donation-create'),
    path('dashboard/donations/<int:pk>/edit/', views_crud.DonationUpdateView.as_view(), name='donation-update'),
    path('dashboard/donations/<int:pk>/delete/', views_crud.DonationDeleteView.as_view(), name='donation-delete'),
    
    # Sponsors - Deliverables
    path('dashboard/deliverables/', views_crud.DeliverableListView.as_view(), name='deliverable-list'),
    path('dashboard/deliverables/create/', views_crud.DeliverableCreateView.as_view(), name='deliverable-create'),
    path('dashboard/deliverables/<int:pk>/edit/', views_crud.DeliverableUpdateView.as_view(), name='deliverable-update'),
    path('dashboard/deliverables/<int:pk>/delete/', views_crud.DeliverableDeleteView.as_view(), name='deliverable-delete'),
    
    # Sponsors - Assets
    path('dashboard/assets/', views_crud.SponsorAssetListView.as_view(), name='asset-list'),
    path('dashboard/assets/create/', views_crud.SponsorAssetCreateView.as_view(), name='asset-create'),
    path('dashboard/assets/<int:pk>/delete/', views_crud.SponsorAssetDeleteView.as_view(), name='asset-delete'),
    
    # CMS - Pages
    path('dashboard/pages/', views_crud.PageListView.as_view(), name='page-list'),
    path('dashboard/pages/create/', views_crud.PageCreateView.as_view(), name='page-create'),
    path('dashboard/pages/<uuid:pk>/edit/', views_crud.PageUpdateView.as_view(), name='page-update'),
    path('dashboard/pages/<uuid:pk>/delete/', views_crud.PageDeleteView.as_view(), name='page-delete'),
    
    # CMS - Menus
    path('dashboard/menus/', views_crud.MenuListView.as_view(), name='menu-list'),
    path('dashboard/menus/create/', views_crud.MenuCreateView.as_view(), name='menu-create'),
    path('dashboard/menus/<int:pk>/edit/', views_crud.MenuUpdateView.as_view(), name='menu-update'),
    path('dashboard/menus/<int:pk>/delete/', views_crud.MenuDeleteView.as_view(), name='menu-delete'),
    
    # CMS - Menu Items
    path('dashboard/menu-items/', views_crud.MenuItemListView.as_view(), name='menuitem-list'),
    path('dashboard/menu-items/create/', views_crud.MenuItemCreateView.as_view(), name='menuitem-create'),
    path('dashboard/menu-items/<int:pk>/edit/', views_crud.MenuItemUpdateView.as_view(), name='menuitem-update'),
    path('dashboard/menu-items/<int:pk>/delete/', views_crud.MenuItemDeleteView.as_view(), name='menuitem-delete'),
    
    # CMS - Site Settings
    path('dashboard/settings/', views_crud.SiteSettingListView.as_view(), name='setting-list'),
    path('dashboard/settings/create/', views_crud.SiteSettingCreateView.as_view(), name='setting-create'),
    path('dashboard/settings/<int:pk>/edit/', views_crud.SiteSettingUpdateView.as_view(), name='setting-update'),
    path('dashboard/settings/<int:pk>/delete/', views_crud.SiteSettingDeleteView.as_view(), name='setting-delete'),
    
    # CMS - Widgets
    path('dashboard/widgets/', views_crud.WidgetListView.as_view(), name='widget-list'),
    path('dashboard/widgets/create/', views_crud.WidgetCreateView.as_view(), name='widget-create'),
    path('dashboard/widgets/<int:pk>/edit/', views_crud.WidgetUpdateView.as_view(), name='widget-update'),
    path('dashboard/widgets/<int:pk>/delete/', views_crud.WidgetDeleteView.as_view(), name='widget-delete'),
    
    # CMS - Media Library
    path('dashboard/media/', views_crud.MediaLibraryListView.as_view(), name='media-list'),
    path('dashboard/media/upload/', views_crud.MediaLibraryCreateView.as_view(), name='media-create'),
    path('dashboard/media/<uuid:pk>/delete/', views_crud.MediaLibraryDeleteView.as_view(), name='media-delete'),
    
    # Organization Profile
    path('dashboard/organization/', views_crud.OrganizationProfileUpdateView.as_view(), name='organization-edit'),
    
    # Analytics Dashboard
    path('dashboard/analytics/', views_crud.AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
    
    # Public Pages
    path('videos/', views_crud.public_videos, name='public-videos'),
    path('videos/<slug:slug>/', views_crud.public_video_detail, name='public-video-detail'),
    path('blog/', views_crud.public_blog, name='public-blog'),
    path('blog/<slug:slug>/', views_crud.public_blog_detail, name='public-blog-detail'),
    path('donate/', views_crud.public_donate, name='donate'),
    path('newsletter/', views_crud.public_newsletter, name='newsletter'),
    path('about/', views_crud.public_about, name='about'),
    path('contact/', views_crud.public_contact, name='contact'),

    # Profile
    path('dashboard/profile/', views_profile.profile, name='profile'),
    
    # Existing API documentation and main pages
    path('api/docs/', views.api_docs, name='api_docs'),
    path('home/', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('config/', views.config_page, name='config'),
    path('v2/', views.v2_page, name='v2'),
    
    # Manuals & Documentation Hub
    path('manuals/', views.manuals_page, name='manuals'),
    path('manual/', views.manual_page, name='manual'),
    
    # Frontend Pages
    path('settings/', views.settings_page, name='settings'),
    path('profile/', views.profile_page, name='profile_page'),
    path('content/', views.content_page, name='content'),
]
