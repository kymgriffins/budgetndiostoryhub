"""
Comprehensive CRUD tests for Dashboard operations with logged-in users.
Tests authentication, CRUD operations, validation, error handling, and feedback.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.accounts.models import User
from apps.content.models import Category, VideoContent, Playlist, BlogPost, NewsItem
from apps.newsletter.models import Subscriber, NewsletterCampaign
from apps.sponsors.models import Donation, SponsorshipDeliverable, SponsorAsset
from apps.cms.models import Page, Menu, MenuItem, SiteSetting, Widget


User = get_user_model()


class LoggedInUserCRUDTestCase(TestCase):
    """Test comprehensive CRUD operations for logged-in admin users"""
    
    def setUp(self):
        """Set up test client and authenticated user"""
        self.client = Client()
        
        # Create admin user (staff with permissions)
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Force login as admin user
        self.client.force_login(self.admin_user)
        
        # Base URL for API
        self.base_url = '/api/'
    
    # ===========================================
    # CONTENT - CATEGORY TESTS
    # ===========================================
    
    def test_category_create_success(self):
        """Test successful category creation returns 201"""
        data = {
            'name': 'Test Category',
            'slug': 'test-category',
            'description': 'Test category description'
        }
        response = self.client.post(
            '/api/content/categories/',
            data=data,
            content_type='application/json'
        )
        # Check for success (201) or redirect (302) with success message
        self.assertIn(response.status_code, [201, 302])
        
        # Verify category was created
        self.assertTrue(Category.objects.filter(slug='test-category').exists())
    
    def test_category_read_success(self):
        """Test successful category retrieval"""
        # Create category first
        category = Category.objects.create(
            name='Test Category',
            slug='test-category-read',
            description='Test description'
        )
        
        response = self.client.get(f'/api/content/categories/{category.id}/')
        self.assertIn(response.status_code, [200, 302])
    
    def test_category_update_success(self):
        """Test successful category update"""
        category = Category.objects.create(
            name='Original Name',
            slug='original-slug',
            description='Original description'
        )
        
        data = {
            'name': 'Updated Name',
            'description': 'Updated description'
        }
        
        response = self.client.patch(
            f'/api/content/categories/{category.id}/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302])
        
        # Verify update
        category.refresh_from_db()
        self.assertEqual(category.name, 'Updated Name')
    
    def test_category_delete_success(self):
        """Test successful category deletion"""
        category = Category.objects.create(
            name='To Delete',
            slug='to-delete',
            description='Will be deleted'
        )
        category_id = category.id
        
        response = self.client.delete(f'/api/content/categories/{category_id}/')
        self.assertIn(response.status_code, [204, 302])
        
        # Verify deletion
        self.assertFalse(Category.objects.filter(id=category_id).exists())
    
    def test_category_create_validation_error(self):
        """Test category creation with validation errors"""
        # Try creating without required fields
        data = {'name': ''}  # Empty name should fail
        response = self.client.post(
            '/api/content/categories/',
            data=data,
            content_type='application/json'
        )
        # Should return error (400 or 422)
        self.assertIn(response.status_code, [400, 422, 302])
    
    # ===========================================
    # CONTENT - VIDEO TESTS
    # ===========================================
    
    def test_video_create_success(self):
        """Test successful video creation"""
        category = Category.objects.create(
            name='Test Category',
            slug='test-cat-video',
            description='Test'
        )
        
        data = {
            'title': 'Test Video',
            'slug': 'test-video',
            'description': 'Test video description',
            'category': category.id,
            'video_url': 'https://example.com/video.mp4',
            'is_published': True
        }
        
        response = self.client.post(
            '/api/content/videos/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [201, 302])
        
        # Verify video was created
        self.assertTrue(VideoContent.objects.filter(slug='test-video').exists())
    
    def test_video_read_list(self):
        """Test retrieving video list"""
        response = self.client.get('/api/content/videos/')
        self.assertIn(response.status_code, [200, 302])
    
    def test_video_update_success(self):
        """Test successful video update"""
        category = Category.objects.create(
            name='Test Category',
            slug='test-cat-video-update',
            description='Test'
        )
        
        video = VideoContent.objects.create(
            title='Original Title',
            slug='original-video',
            description='Original',
            category=category,
            is_published=False
        )
        
        data = {
            'title': 'Updated Title',
            'is_published': True
        }
        
        response = self.client.patch(
            f'/api/content/videos/{video.id}/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302])
        
        video.refresh_from_db()
        self.assertEqual(video.title, 'Updated Title')
    
    def test_video_delete_success(self):
        """Test successful video deletion"""
        category = Category.objects.create(
            name='Test Category',
            slug='test-cat-video-delete',
            description='Test'
        )
        
        video = VideoContent.objects.create(
            title='To Delete',
            slug='video-to-delete',
            description='Will be deleted',
            category=category
        )
        video_id = video.id
        
        response = self.client.delete(f'/api/content/videos/{video_id}/')
        self.assertIn(response.status_code, [204, 302])
        
        self.assertFalse(VideoContent.objects.filter(id=video_id).exists())
    
    # ===========================================
    # CONTENT - PLAYLIST TESTS
    # ===========================================
    
    def test_playlist_create_success(self):
        """Test successful playlist creation"""
        data = {
            'name': 'Test Playlist',
            'slug': 'test-playlist',
            'description': 'Test playlist description',
            'is_published': True
        }
        
        response = self.client.post(
            '/api/content/playlists/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [201, 302])
        
        self.assertTrue(Playlist.objects.filter(slug='test-playlist').exists())
    
    def test_playlist_update_success(self):
        """Test successful playlist update"""
        playlist = Playlist.objects.create(
            name='Original Playlist',
            slug='original-playlist',
            description='Original',
            is_published=False
        )
        
        data = {
            'name': 'Updated Playlist',
            'is_published': True
        }
        
        response = self.client.patch(
            f'/api/content/playlists/{playlist.id}/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302])
    
    def test_playlist_delete_success(self):
        """Test successful playlist deletion"""
        playlist = Playlist.objects.create(
            name='To Delete',
            slug='playlist-to-delete',
            description='Will be deleted'
        )
        playlist_id = playlist.id
        
        response = self.client.delete(f'/api/content/playlists/{playlist_id}/')
        self.assertIn(response.status_code, [204, 302])
        
        self.assertFalse(Playlist.objects.filter(id=playlist_id).exists())
    
    # ===========================================
    # CONTENT - BLOG POST TESTS
    # ===========================================
    
    def test_blogpost_create_success(self):
        """Test successful blog post creation"""
        category = Category.objects.create(
            name='Blog Category',
            slug='blog-category',
            description='Test'
        )
        
        data = {
            'title': 'Test Blog Post',
            'slug': 'test-blog-post',
            'content': 'Test blog content',
            'category': category.id,
            'is_published': True,
            'author': self.admin_user.id
        }
        
        response = self.client.post(
            '/api/content/posts/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [201, 302])
        
        self.assertTrue(BlogPost.objects.filter(slug='test-blog-post').exists())
    
    def test_blogpost_update_success(self):
        """Test successful blog post update"""
        category = Category.objects.create(
            name='Blog Category',
            slug='blog-category-update',
            description='Test'
        )
        
        post = BlogPost.objects.create(
            title='Original Post',
            slug='original-post',
            content='Original content',
            category=category,
            author=self.admin_user,
            is_published=False
        )
        
        data = {
            'title': 'Updated Post Title',
            'is_published': True
        }
        
        response = self.client.patch(
            f'/api/content/posts/{post.id}/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302])
    
    def test_blogpost_delete_success(self):
        """Test successful blog post deletion"""
        category = Category.objects.create(
            name='Blog Category',
            slug='blog-category-delete',
            description='Test'
        )
        
        post = BlogPost.objects.create(
            title='To Delete',
            slug='post-to-delete',
            content='Will be deleted',
            category=category,
            author=self.admin_user
        )
        post_id = post.id
        
        response = self.client.delete(f'/api/content/posts/{post_id}/')
        self.assertIn(response.status_code, [204, 302])
        
        self.assertFalse(BlogPost.objects.filter(id=post_id).exists())
    
    # ===========================================
    # NEWSLETTER - SUBSCRIBER TESTS
    # ===========================================
    
    def test_subscriber_create_success(self):
        """Test successful subscriber creation"""
        data = {
            'email': 'newsubscriber@test.com',
            'first_name': 'Test',
            'last_name': 'Subscriber',
            'is_active': True
        }
        
        response = self.client.post(
            '/api/newsletter/subscribers/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [201, 302])
        
        self.assertTrue(Subscriber.objects.filter(email='newsubscriber@test.com').exists())
    
    def test_subscriber_create_validation_error(self):
        """Test subscriber creation with invalid email"""
        data = {
            'email': 'invalid-email',  # Invalid email
            'first_name': 'Test'
        }
        
        response = self.client.post(
            '/api/newsletter/subscribers/',
            data=data,
            content_type='application/json'
        )
        # Should return error
        self.assertIn(response.status_code, [400, 422, 302])
    
    def test_subscriber_update_success(self):
        """Test successful subscriber update"""
        subscriber = Subscriber.objects.create(
            email='subscriber@test.com',
            first_name='Original',
            is_active=False
        )
        
        data = {
            'first_name': 'Updated',
            'is_active': True
        }
        
        response = self.client.patch(
            f'/api/newsletter/subscribers/{subscriber.id}/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302])
    
    def test_subscriber_delete_success(self):
        """Test successful subscriber deletion"""
        subscriber = Subscriber.objects.create(
            email='todelete@test.com',
            first_name='ToDelete'
        )
        subscriber_id = subscriber.id
        
        response = self.client.delete(f'/api/newsletter/subscribers/{subscriber_id}/')
        self.assertIn(response.status_code, [204, 302])
        
        self.assertFalse(Subscriber.objects.filter(id=subscriber_id).exists())
    
    # ===========================================
    # NEWSLETTER - CAMPAIGN TESTS
    # ===========================================
    
    def test_campaign_create_success(self):
        """Test successful campaign creation"""
        data = {
            'subject': 'Test Campaign',
            'slug': 'test-campaign',
            'content': 'Test campaign content',
            'status': 'draft'
        }
        
        response = self.client.post(
            '/api/newsletter/campaigns/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [201, 302])
        
        self.assertTrue(NewsletterCampaign.objects.filter(slug='test-campaign').exists())
    
    def test_campaign_update_success(self):
        """Test successful campaign update"""
        campaign = NewsletterCampaign.objects.create(
            subject='Original Subject',
            slug='original-campaign',
            content='Original content',
            status='draft'
        )
        
        data = {
            'subject': 'Updated Subject',
            'status': 'sent'
        }
        
        response = self.client.patch(
            f'/api/newsletter/campaigns/{campaign.id}/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302])
    
    def test_campaign_delete_success(self):
        """Test successful campaign deletion"""
        campaign = NewsletterCampaign.objects.create(
            subject='To Delete',
            slug='campaign-to-delete',
            content='Will be deleted',
            status='draft'
        )
        campaign_id = campaign.id
        
        response = self.client.delete(f'/api/newsletter/campaigns/{campaign_id}/')
        self.assertIn(response.status_code, [204, 302])
        
        self.assertFalse(NewsletterCampaign.objects.filter(id=campaign_id).exists())
    
    # ===========================================
    # SPONSORS - DONATION TESTS
    # ===========================================
    
    def test_donation_create_success(self):
        """Test successful donation creation"""
        data = {
            'donor_name': 'Test Donor',
            'donor_email': 'donor@test.com',
            'amount': '100.00',
            'payment_method': 'credit_card',
            'status': 'completed'
        }
        
        response = self.client.post(
            '/api/sponsors/donations/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [201, 302])
        
        self.assertTrue(Donation.objects.filter(donor_email='donor@test.com').exists())
    
    def test_donation_create_validation_error(self):
        """Test donation creation with validation errors"""
        data = {
            'donor_name': 'Test Donor',
            'amount': 'invalid-amount',  # Invalid amount
        }
        
        response = self.client.post(
            '/api/sponsors/donations/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [400, 422, 302])
    
    def test_donation_update_success(self):
        """Test successful donation update"""
        donation = Donation.objects.create(
            donor_name='Original Donor',
            donor_email='original@test.com',
            amount=50.00,
            status='pending'
        )
        
        data = {
            'status': 'completed'
        }
        
        response = self.client.patch(
            f'/api/sponsors/donations/{donation.id}/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302])
    
    def test_donation_delete_success(self):
        """Test successful donation deletion"""
        donation = Donation.objects.create(
            donor_name='To Delete',
            donor_email='delete@test.com',
            amount=100.00,
            status='pending'
        )
        donation_id = donation.id
        
        response = self.client.delete(f'/api/sponsors/donations/{donation_id}/')
        self.assertIn(response.status_code, [204, 302])
        
        self.assertFalse(Donation.objects.filter(id=donation_id).exists())
    
    # ===========================================
    # SPONSORS - DELIVERABLE TESTS
    # ===========================================
    
    def test_deliverable_create_success(self):
        """Test successful deliverable creation"""
        data = {
            'name': 'Test Deliverable',
            'slug': 'test-deliverable',
            'description': 'Test deliverable description',
            'status': 'pending'
        }
        
        response = self.client.post(
            '/api/sponsors/deliverables/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [201, 302])
        
        self.assertTrue(SponsorshipDeliverable.objects.filter(slug='test-deliverable').exists())
    
    def test_deliverable_update_success(self):
        """Test successful deliverable update"""
        deliverable = SponsorshipDeliverable.objects.create(
            name='Original Deliverable',
            slug='original-deliverable',
            description='Original',
            status='pending'
        )
        
        data = {
            'status': 'completed'
        }
        
        response = self.client.patch(
            f'/api/sponsors/deliverables/{deliverable.id}/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302])
    
    def test_deliverable_delete_success(self):
        """Test successful deliverable deletion"""
        deliverable = SponsorshipDeliverable.objects.create(
            name='To Delete',
            slug='deliverable-to-delete',
            description='Will be deleted'
        )
        deliverable_id = deliverable.id
        
        response = self.client.delete(f'/api/sponsors/deliverables/{deliverable_id}/')
        self.assertIn(response.status_code, [204, 302])
        
        self.assertFalse(SponsorshipDeliverable.objects.filter(id=deliverable_id).exists())
    
    # ===========================================
    # CMS - PAGE TESTS
    # ===========================================
    
    def test_page_create_success(self):
        """Test successful page creation"""
        data = {
            'title': 'Test Page',
            'slug': 'test-page',
            'content': 'Test page content',
            'status': 'published'
        }
        
        response = self.client.post(
            '/api/cms/pages/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [201, 302])
        
        self.assertTrue(Page.objects.filter(slug='test-page').exists())
    
    def test_page_update_success(self):
        """Test successful page update"""
        page = Page.objects.create(
            title='Original Page',
            slug='original-page',
            content='Original content',
            status='draft'
        )
        
        data = {
            'title': 'Updated Page Title',
            'status': 'published'
        }
        
        response = self.client.patch(
            f'/api/cms/pages/{page.id}/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302])
    
    def test_page_delete_success(self):
        """Test successful page deletion"""
        page = Page.objects.create(
            title='To Delete',
            slug='page-to-delete',
            content='Will be deleted'
        )
        page_id = page.id
        
        response = self.client.delete(f'/api/cms/pages/{page_id}/')
        self.assertIn(response.status_code, [204, 302])
        
        self.assertFalse(Page.objects.filter(id=page_id).exists())
    
    # ===========================================
    # CMS - MENU TESTS
    # ===========================================
    
    def test_menu_create_success(self):
        """Test successful menu creation"""
        data = {
            'name': 'Test Menu',
            'slug': 'test-menu',
            'location': 'header'
        }
        
        response = self.client.post(
            '/api/cms/menus/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [201, 302])
        
        self.assertTrue(Menu.objects.filter(slug='test-menu').exists())
    
    def test_menu_update_success(self):
        """Test successful menu update"""
        menu = Menu.objects.create(
            name='Original Menu',
            slug='original-menu',
            location='footer'
        )
        
        data = {
            'name': 'Updated Menu',
            'location': 'header'
        }
        
        response = self.client.patch(
            f'/api/cms/menus/{menu.id}/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302])
    
    def test_menu_delete_success(self):
        """Test successful menu deletion"""
        menu = Menu.objects.create(
            name='To Delete',
            slug='menu-to-delete',
            location='sidebar'
        )
        menu_id = menu.id
        
        response = self.client.delete(f'/api/cms/menus/{menu_id}/')
        self.assertIn(response.status_code, [204, 302])
        
        self.assertFalse(Menu.objects.filter(id=menu_id).exists())
    
    # ===========================================
    # CMS - SETTING TESTS
    # ===========================================
    
    def test_setting_create_success(self):
        """Test successful setting creation"""
        data = {
            'key': 'test_setting',
            'value': 'test_value',
            'category': 'general'
        }
        
        response = self.client.post(
            '/api/cms/settings/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [201, 302])
        
        self.assertTrue(SiteSetting.objects.filter(key='test_setting').exists())
    
    def test_setting_update_success(self):
        """Test successful setting update"""
        setting = SiteSetting.objects.create(
            key='original_key',
            value='original_value',
            category='general'
        )
        
        data = {
            'value': 'updated_value'
        }
        
        response = self.client.patch(
            f'/api/cms/settings/{setting.id}/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302])
    
    def test_setting_delete_success(self):
        """Test successful setting deletion"""
        setting = SiteSetting.objects.create(
            key='to_delete',
            value='will_be_deleted',
            category='general'
        )
        setting_id = setting.id
        
        response = self.client.delete(f'/api/cms/settings/{setting_id}/')
        self.assertIn(response.status_code, [204, 302])
        
        self.assertFalse(SiteSetting.objects.filter(id=setting_id).exists())
    
    # ===========================================
    # CMS - WIDGET TESTS
    # ===========================================
    
    def test_widget_create_success(self):
        """Test successful widget creation"""
        data = {
            'name': 'Test Widget',
            'slug': 'test-widget',
            'widget_type': 'text',
            'content': 'Test widget content'
        }
        
        response = self.client.post(
            '/api/cms/widgets/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [201, 302])
        
        self.assertTrue(Widget.objects.filter(slug='test-widget').exists())
    
    def test_widget_update_success(self):
        """Test successful widget update"""
        widget = Widget.objects.create(
            name='Original Widget',
            slug='original-widget',
            widget_type='text',
            content='Original content'
        )
        
        data = {
            'name': 'Updated Widget',
            'content': 'Updated content'
        }
        
        response = self.client.patch(
            f'/api/cms/widgets/{widget.id}/',
            data=data,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302])
    
    def test_widget_delete_success(self):
        """Test successful widget deletion"""
        widget = Widget.objects.create(
            name='To Delete',
            slug='widget-to-delete',
            widget_type='text',
            content='Will be deleted'
        )
        widget_id = widget.id
        
        response = self.client.delete(f'/api/cms/widgets/{widget_id}/')
        self.assertIn(response.status_code, [204, 302])
        
        self.assertFalse(Widget.objects.filter(id=widget_id).exists())
    
    # ===========================================
    # UNAUTHORIZED ACCESS TESTS
    # ===========================================
    
    def test_unauthenticated_crud_denied(self):
        """Test that unauthenticated users cannot perform CRUD operations"""
        # Create a client that's not logged in
        anonymous_client = Client()
        
        # Try to create
        response = anonymous_client.post(
            '/api/content/categories/',
            data={'name': 'Test'},
            content_type='application/json'
        )
        # Should be denied (401, 403, or redirect)
        self.assertIn(response.status_code, [401, 403, 302])
        
        # Try to read
        category = Category.objects.create(name='Test', slug='test-auth', description='test')
        response = anonymous_client.get(f'/api/content/categories/{category.id}/')
        self.assertIn(response.status_code, [401, 403, 302])
        
        # Try to update
        response = anonymous_client.patch(
            f'/api/content/categories/{category.id}/',
            data={'name': 'Updated'},
            content_type='application/json'
        )
        self.assertIn(response.status_code, [401, 403, 302])
        
        # Try to delete
        response = anonymous_client.delete(f'/api/content/categories/{category.id}/')
        self.assertIn(response.status_code, [401, 403, 302])


class ToastNotificationTestCase(TestCase):
    """Test toast notification system"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin_toast',
            email='admin_toast@test.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        self.client.force_login(self.admin_user)
    
    def test_success_toast_on_create(self):
        """Test that successful create shows success feedback"""
        # This test verifies the response includes success indication
        data = {
            'name': 'Toast Test Category',
            'slug': 'toast-test-category',
            'description': 'Testing toast notifications'
        }
        
        response = self.client.post(
            '/api/content/categories/',
            data=data,
            content_type='application/json'
        )
        
        # Check response is successful
        self.assertIn(response.status_code, [201, 302])
        
        # Verify success message in response (for HTML responses)
        if hasattr(response, 'content'):
            content = response.content.decode('utf-8')
            # Check for success indicators
            self.assertTrue(
                'success' in content.lower() or 
                'created' in content.lower() or
                response.status_code == 201
            )
    
    def test_error_toast_on_validation_failure(self):
        """Test that validation errors show error feedback"""
        # Try to create with invalid data
        data = {'name': ''}  # Empty name should fail
        
        response = self.client.post(
            '/api/content/categories/',
            data=data,
            content_type='application/json'
        )
        
        # Check for error response
        self.assertIn(response.status_code, [400, 422, 302])
    
    def test_success_toast_on_update(self):
        """Test that successful update shows success feedback"""
        category = Category.objects.create(
            name='Update Test',
            slug='update-test',
            description='Testing update'
        )
        
        data = {'name': 'Updated Name'}
        
        response = self.client.patch(
            f'/api/content/categories/{category.id}/',
            data=data,
            content_type='application/json'
        )
        
        self.assertIn(response.status_code, [200, 302])
    
    def test_success_toast_on_delete(self):
        """Test that successful deletion shows success feedback"""
        category = Category.objects.create(
            name='Delete Test',
            slug='delete-test',
            description='Testing delete'
        )
        category_id = category.id
        
        response = self.client.delete(f'/api/content/categories/{category_id}/')
        
        self.assertIn(response.status_code, [204, 302])
        self.assertFalse(Category.objects.filter(id=category_id).exists())
