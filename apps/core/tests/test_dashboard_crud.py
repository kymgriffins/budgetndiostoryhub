"""
Comprehensive tests for Dashboard CRUD operations.
Tests authentication protection, CRUD functionality, filtering, and error handling.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.accounts.models import User, DonorProfile, SponsorProfile, ConsortiumPartner
from apps.content.models import Category, VideoContent, Playlist, BlogPost, NewsItem
from apps.newsletter.models import Subscriber, NewsletterCampaign
from apps.sponsors.models import Donation, SponsorshipDeliverable, SponsorAsset
from apps.cms.models import Page, Menu, MenuItem, SiteSetting, Widget, MediaLibrary


User = get_user_model()


class DashboardAuthenticationTestCase(TestCase):
    """Test that all dashboard routes require authentication"""
    
    def setUp(self):
        """Set up test client and users"""
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@test.com',
            password='regularpass123',
            is_staff=False
        )
        
        # Dashboard URLs to test
        self.dashboard_urls = [
            '/dashboard/',
            '/dashboard/categories/',
            '/dashboard/videos/',
            '/dashboard/playlists/',
            '/dashboard/posts/',
            '/dashboard/news/',
            '/dashboard/subscribers/',
            '/dashboard/campaigns/',
            '/dashboard/donations/',
            '/dashboard/deliverables/',
            '/dashboard/assets/',
            '/dashboard/pages/',
            '/dashboard/menus/',
            '/dashboard/menu-items/',
            '/dashboard/settings/',
            '/dashboard/widgets/',
            '/dashboard/media/',
            '/dashboard/analytics/',
            '/dashboard/users/',
            '/dashboard/donors/',
            '/dashboard/sponsors/',
            '/dashboard/partners/',
        ]
    
    def test_unauthenticated_user_redirected_to_login(self):
        """Test that unauthenticated users are redirected to login"""
        for url in self.dashboard_urls[:5]:  # Test first 5 URLs
            response = self.client.get(url)
            # Should either redirect or return 302
            self.assertIn(response.status_code, [302, 403, 401])
    
    def test_regular_user_denied_access(self):
        """Test that non-staff users are denied access"""
        self.client.force_login(self.regular_user)
        
        for url in self.dashboard_urls[:5]:
            response = self.client.get(url)
            # Should return 403 Forbidden
            self.assertEqual(response.status_code, 403)
    
    def test_admin_user_can_access_dashboard(self):
        """Test that admin users can access dashboard"""
        self.client.force_login(self.admin_user)
        
        # Test main dashboard
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        
        # Test a few key pages
        response = self.client.get('/dashboard/categories/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/dashboard/users/')
        self.assertEqual(response.status_code, 200)


class CategoryCRUDTestCase(TestCase):
    """Test Category CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.force_login(self.admin_user)
        
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            description='Test description',
            is_active=True,
            order=1
        )
    
    def test_category_list_view(self):
        """Test category list displays correctly"""
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')
    
    def test_category_create_view(self):
        """Test category creation"""
        response = self.client.post(reverse('category-create'), {
            'name': 'New Category',
            'slug': 'new-category',
            'description': 'New description',
            'is_active': True,
            'order': 2
        })
        # Should redirect after successful creation
        self.assertIn(response.status_code, [302, 200])
        
        # Verify category was created
        self.assertTrue(Category.objects.filter(slug='new-category').exists())
    
    def test_category_update_view(self):
        """Test category update"""
        response = self.client.post(
            reverse('category-update', kwargs={'pk': self.category.pk}),
            {
                'name': 'Updated Category',
                'slug': 'test-category',
                'description': 'Updated description',
                'is_active': False,
                'order': 1
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify category was updated
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')
        self.assertFalse(self.category.is_active)
    
    def test_category_delete_view(self):
        """Test category deletion"""
        category_id = self.category.pk
        response = self.client.post(reverse('category-delete', kwargs={'pk': category_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify category was deleted
        self.assertFalse(Category.objects.filter(pk=category_id).exists())


class VideoCRUDTestCase(TestCase):
    """Test Video Content CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        self.video = VideoContent.objects.create(
            title='Test Video',
            slug='test-video',
            platform='youtube',
            external_id='abc123',
            external_url='https://youtube.com/watch?v=abc123',
            content_type='budget_basics',
            is_published=True
        )
    
    def test_video_list_view(self):
        """Test video list displays correctly"""
        response = self.client.get(reverse('video-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Video')
    
    def test_video_create_view(self):
        """Test video creation"""
        response = self.client.post(reverse('video-create'), {
            'title': 'New Video',
            'slug': 'new-video',
            'platform': 'tiktok',
            'external_id': 'xyz789',
            'external_url': 'https://tiktok.com/@user/video/xyz789',
            'content_type': 'national_budget',
            'is_published': True
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify video was created
        self.assertTrue(VideoContent.objects.filter(slug='new-video').exists())
    
    def test_video_update_view(self):
        """Test video update"""
        response = self.client.post(
            reverse('video-update', kwargs={'pk': self.video.pk}),
            {
                'title': 'Updated Video',
                'slug': 'test-video',
                'platform': 'youtube',
                'external_id': 'abc123',
                'external_url': 'https://youtube.com/watch?v=abc123',
                'content_type': 'budget_basics',
                'is_published': False
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify video was updated
        self.video.refresh_from_db()
        self.assertEqual(self.video.title, 'Updated Video')
        self.assertFalse(self.video.is_published)
    
    def test_video_delete_view(self):
        """Test video deletion"""
        video_id = self.video.pk
        response = self.client.post(reverse('video-delete', kwargs={'pk': video_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify video was deleted
        self.assertFalse(VideoContent.objects.filter(pk=video_id).exists())


class PlaylistCRUDTestCase(TestCase):
    """Test Playlist CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        self.playlist = Playlist.objects.create(
            title='Test Playlist',
            slug='test-playlist',
            description='Test description',
            difficulty_level='beginner'
        )
    
    def test_playlist_list_view(self):
        """Test playlist list displays correctly"""
        response = self.client.get(reverse('playlist-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Playlist')
    
    def test_playlist_create_view(self):
        """Test playlist creation"""
        response = self.client.post(reverse('playlist-create'), {
            'title': 'New Playlist',
            'slug': 'new-playlist',
            'description': 'New description',
            'difficulty_level': 'intermediate'
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify playlist was created
        self.assertTrue(Playlist.objects.filter(slug='new-playlist').exists())
    
    def test_playlist_update_view(self):
        """Test playlist update"""
        response = self.client.post(
            reverse('playlist-update', kwargs={'pk': self.playlist.pk}),
            {
                'title': 'Updated Playlist',
                'slug': 'test-playlist',
                'description': 'Updated description',
                'difficulty_level': 'advanced'
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify playlist was updated
        self.playlist.refresh_from_db()
        self.assertEqual(self.playlist.title, 'Updated Playlist')
        self.assertEqual(self.playlist.difficulty_level, 'advanced')
    
    def test_playlist_delete_view(self):
        """Test playlist deletion"""
        playlist_id = self.playlist.pk
        response = self.client.post(reverse('playlist-delete', kwargs={'pk': playlist_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify playlist was deleted
        self.assertFalse(Playlist.objects.filter(pk=playlist_id).exists())


class BlogPostCRUDTestCase(TestCase):
    """Test BlogPost CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        self.post = BlogPost.objects.create(
            title='Test Post',
            slug='test-post',
            content='Test content',
            post_type='investigation',
            status='draft',
            author=self.admin_user
        )
    
    def test_blogpost_list_view(self):
        """Test blog post list displays correctly"""
        response = self.client.get(reverse('blogpost-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
    
    def test_blogpost_create_view(self):
        """Test blog post creation"""
        response = self.client.post(reverse('blogpost-create'), {
            'title': 'New Post',
            'slug': 'new-post',
            'content': 'New content',
            'post_type': 'explainer',
            'status': 'draft',
            'author': self.admin_user.pk
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify post was created
        self.assertTrue(BlogPost.objects.filter(slug='new-post').exists())
    
    def test_blogpost_update_view(self):
        """Test blog post update"""
        response = self.client.post(
            reverse('blogpost-update', kwargs={'pk': self.post.pk}),
            {
                'title': 'Updated Post',
                'slug': 'test-post',
                'content': 'Updated content',
                'post_type': 'investigation',
                'status': 'published',
                'author': self.admin_user.pk
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify post was updated
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')
        self.assertEqual(self.post.status, 'published')
    
    def test_blogpost_delete_view(self):
        """Test blog post deletion"""
        post_id = self.post.pk
        response = self.client.post(reverse('blogpost-delete', kwargs={'pk': post_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify post was deleted
        self.assertFalse(BlogPost.objects.filter(pk=post_id).exists())


class SubscriberCRUDTestCase(TestCase):
    """Test Subscriber CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        self.subscriber = Subscriber.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            status='active'
        )
    
    def test_subscriber_list_view(self):
        """Test subscriber list displays correctly"""
        response = self.client.get(reverse('subscriber-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test@example.com')
    
    def test_subscriber_create_view(self):
        """Test subscriber creation"""
        response = self.client.post(reverse('subscriber-create'), {
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'status': 'pending'
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify subscriber was created
        self.assertTrue(Subscriber.objects.filter(email='new@example.com').exists())
    
    def test_subscriber_update_view(self):
        """Test subscriber update"""
        response = self.client.post(
            reverse('subscriber-update', kwargs={'pk': self.subscriber.pk}),
            {
                'email': 'test@example.com',
                'first_name': 'Updated',
                'last_name': 'User',
                'status': 'unsubscribed'
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify subscriber was updated
        self.subscriber.refresh_from_db()
        self.assertEqual(self.subscriber.first_name, 'Updated')
        self.assertEqual(self.subscriber.status, 'unsubscribed')
    
    def test_subscriber_delete_view(self):
        """Test subscriber deletion"""
        subscriber_id = self.subscriber.pk
        response = self.client.post(reverse('subscriber-delete', kwargs={'pk': subscriber_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify subscriber was deleted
        self.assertFalse(Subscriber.objects.filter(pk=subscriber_id).exists())


class CampaignCRUDTestCase(TestCase):
    """Test Newsletter Campaign CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        self.campaign = NewsletterCampaign.objects.create(
            name='Test Campaign',
            subject='Test Subject',
            campaign_type='weekly_digest',
            status='draft'
        )
    
    def test_campaign_list_view(self):
        """Test campaign list displays correctly"""
        response = self.client.get(reverse('campaign-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Campaign')
    
    def test_campaign_create_view(self):
        """Test campaign creation"""
        response = self.client.post(reverse('campaign-create'), {
            'name': 'New Campaign',
            'subject': 'New Subject',
            'campaign_type': 'daily_update',
            'status': 'draft'
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify campaign was created
        self.assertTrue(NewsletterCampaign.objects.filter(name='New Campaign').exists())
    
    def test_campaign_update_view(self):
        """Test campaign update"""
        response = self.client.post(
            reverse('campaign-update', kwargs={'pk': self.campaign.pk}),
            {
                'name': 'Updated Campaign',
                'subject': 'Updated Subject',
                'campaign_type': 'weekly_digest',
                'status': 'scheduled'
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify campaign was updated
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.name, 'Updated Campaign')
        self.assertEqual(self.campaign.status, 'scheduled')
    
    def test_campaign_delete_view(self):
        """Test campaign deletion"""
        campaign_id = self.campaign.pk
        response = self.client.post(reverse('campaign-delete', kwargs={'pk': campaign_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify campaign was deleted
        self.assertFalse(NewsletterCampaign.objects.filter(pk=campaign_id).exists())


class DonationCRUDTestCase(TestCase):
    """Test Donation CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        # Create a donor profile first
        self.donor = DonorProfile.objects.create(
            user=self.admin_user,
            donor_type='individual'
        )
        
        self.donation = Donation.objects.create(
            donor=self.donor,
            amount=100.00,
            currency='KES',
            payment_method='mpesa',
            status='pending'
        )
    
    def test_donation_list_view(self):
        """Test donation list displays correctly"""
        response = self.client.get(reverse('donation-list'))
        self.assertEqual(response.status_code, 200)
    
    def test_donation_create_view(self):
        """Test donation creation"""
        response = self.client.post(reverse('donation-create'), {
            'donor': self.donor.pk,
            'amount': 500.00,
            'currency': 'KES',
            'payment_method': 'card',
            'status': 'pending'
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify donation was created
        self.assertTrue(Donation.objects.filter(amount=500.00).exists())
    
    def test_donation_update_view(self):
        """Test donation update"""
        response = self.client.post(
            reverse('donation-update', kwargs={'pk': self.donation.pk}),
            {
                'donor': self.donor.pk,
                'amount': 200.00,
                'currency': 'KES',
                'payment_method': 'mpesa',
                'status': 'completed'
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify donation was updated
        self.donation.refresh_from_db()
        self.assertEqual(self.donation.amount, 200.00)
        self.assertEqual(self.donation.status, 'completed')
    
    def test_donation_delete_view(self):
        """Test donation deletion"""
        donation_id = self.donation.pk
        response = self.client.post(reverse('donation-delete', kwargs={'pk': donation_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify donation was deleted
        self.assertFalse(Donation.objects.filter(pk=donation_id).exists())


class PageCRUDTestCase(TestCase):
    """Test CMS Page CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        self.page = Page.objects.create(
            title='Test Page',
            slug='test-page',
            content='Test content',
            status='draft',
            author=self.admin_user
        )
    
    def test_page_list_view(self):
        """Test page list displays correctly"""
        response = self.client.get(reverse('page-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Page')
    
    def test_page_create_view(self):
        """Test page creation"""
        response = self.client.post(reverse('page-create'), {
            'title': 'New Page',
            'slug': 'new-page',
            'content': 'New content',
            'status': 'draft',
            'author': self.admin_user.pk
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify page was created
        self.assertTrue(Page.objects.filter(slug='new-page').exists())
    
    def test_page_update_view(self):
        """Test page update"""
        response = self.client.post(
            reverse('page-update', kwargs={'pk': self.page.pk}),
            {
                'title': 'Updated Page',
                'slug': 'test-page',
                'content': 'Updated content',
                'status': 'published',
                'author': self.admin_user.pk
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify page was updated
        self.page.refresh_from_db()
        self.assertEqual(self.page.title, 'Updated Page')
        self.assertEqual(self.page.status, 'published')
    
    def test_page_delete_view(self):
        """Test page deletion"""
        page_id = self.page.pk
        response = self.client.post(reverse('page-delete', kwargs={'pk': page_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify page was deleted
        self.assertFalse(Page.objects.filter(pk=page_id).exists())


class MenuCRUDTestCase(TestCase):
    """Test CMS Menu CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        self.menu = Menu.objects.create(
            name='Test Menu',
            slug='test-menu',
            location='header'
        )
    
    def test_menu_list_view(self):
        """Test menu list displays correctly"""
        response = self.client.get(reverse('menu-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Menu')
    
    def test_menu_create_view(self):
        """Test menu creation"""
        response = self.client.post(reverse('menu-create'), {
            'name': 'New Menu',
            'slug': 'new-menu',
            'location': 'footer'
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify menu was created
        self.assertTrue(Menu.objects.filter(slug='new-menu').exists())
    
    def test_menu_update_view(self):
        """Test menu update"""
        response = self.client.post(
            reverse('menu-update', kwargs={'pk': self.menu.pk}),
            {
                'name': 'Updated Menu',
                'slug': 'test-menu',
                'location': 'footer'
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify menu was updated
        self.menu.refresh_from_db()
        self.assertEqual(self.menu.name, 'Updated Menu')
        self.assertEqual(self.menu.location, 'footer')
    
    def test_menu_delete_view(self):
        """Test menu deletion"""
        menu_id = self.menu.pk
        response = self.client.post(reverse('menu-delete', kwargs={'pk': menu_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify menu was deleted
        self.assertFalse(Menu.objects.filter(pk=menu_id).exists())


class SiteSettingCRUDTestCase(TestCase):
    """Test CMS SiteSetting CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        self.setting = SiteSetting.objects.create(
            key='site_name',
            value='Test Site',
            value_type='text',
            category='general'
        )
    
    def test_setting_list_view(self):
        """Test setting list displays correctly"""
        response = self.client.get(reverse('setting-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'site_name')
    
    def test_setting_create_view(self):
        """Test setting creation"""
        response = self.client.post(reverse('setting-create'), {
            'key': 'new_setting',
            'value': 'New Value',
            'value_type': 'text',
            'category': 'general'
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify setting was created
        self.assertTrue(SiteSetting.objects.filter(key='new_setting').exists())
    
    def test_setting_update_view(self):
        """Test setting update"""
        response = self.client.post(
            reverse('setting-update', kwargs={'pk': self.setting.pk}),
            {
                'key': 'site_name',
                'value': 'Updated Site',
                'value_type': 'text',
                'category': 'general'
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify setting was updated
        self.setting.refresh_from_db()
        self.assertEqual(self.setting.value, 'Updated Site')
    
    def test_setting_delete_view(self):
        """Test setting deletion"""
        setting_id = self.setting.pk
        response = self.client.post(reverse('setting-delete', kwargs={'pk': setting_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify setting was deleted
        self.assertFalse(SiteSetting.objects.filter(pk=setting_id).exists())


class WidgetCRUDTestCase(TestCase):
    """Test CMS Widget CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        self.widget = Widget.objects.create(
            name='Test Widget',
            widget_type='hero'
        )
    
    def test_widget_list_view(self):
        """Test widget list displays correctly"""
        response = self.client.get(reverse('widget-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Widget')
    
    def test_widget_create_view(self):
        """Test widget creation"""
        response = self.client.post(reverse('widget-create'), {
            'name': 'New Widget',
            'widget_type': 'featured_videos'
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify widget was created
        self.assertTrue(Widget.objects.filter(name='New Widget').exists())
    
    def test_widget_update_view(self):
        """Test widget update"""
        response = self.client.post(
            reverse('widget-update', kwargs={'pk': self.widget.pk}),
            {
                'name': 'Updated Widget',
                'widget_type': 'stats'
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify widget was updated
        self.widget.refresh_from_db()
        self.assertEqual(self.widget.name, 'Updated Widget')
    
    def test_widget_delete_view(self):
        """Test widget deletion"""
        widget_id = self.widget.pk
        response = self.client.post(reverse('widget-delete', kwargs={'pk': widget_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify widget was deleted
        self.assertFalse(Widget.objects.filter(pk=widget_id).exists())


class DashboardFilterTestCase(TestCase):
    """Test filtering functionality in dashboard list views"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        # Create test categories
        Category.objects.create(name='Category 1', slug='cat-1', is_active=True)
        Category.objects.create(name='Category 2', slug='cat-2', is_active=False)
    
    def test_category_filter_by_active(self):
        """Test filtering categories by active status"""
        # Test with active filter
        response = self.client.get(reverse('category-list') + '?is_active=true')
        self.assertEqual(response.status_code, 200)
        
        # Test with inactive filter
        response = self.client.get(reverse('category-list') + '?is_active=false')
        self.assertEqual(response.status_code, 200)


class DashboardErrorHandlingTestCase(TestCase):
    """Test error handling in dashboard views"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
    
    def test_invalid_pk_returns_404(self):
        """Test that invalid PK returns 404"""
        response = self.client.get(reverse('category-update', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)
    
    def test_create_with_invalid_data_shows_form_errors(self):
        """Test that invalid form data shows errors"""
        # Try to create category with invalid data (missing required fields)
        response = self.client.post(reverse('category-create'), {
            # Missing required 'name' field
            'slug': 'test'
        })
        # Should return to form with errors (status 200)
        self.assertEqual(response.status_code, 200)
    
    def test_duplicate_slug_shows_error(self):
        """Test that duplicate slug shows validation error"""
        # Create first category
        Category.objects.create(name='Test', slug='duplicate-test')
        
        # Try to create another with same slug
        response = self.client.post(reverse('category-create'), {
            'name': 'Test 2',
            'slug': 'duplicate-test'  # Duplicate slug
        })
        # Should return to form with error
        self.assertEqual(response.status_code, 200)


class DashboardMessagesTestCase(TestCase):
    """Test that success/error messages are properly set"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
    
    def test_category_create_shows_success_message(self):
        """Test that category creation shows success message"""
        response = self.client.post(reverse('category-create'), {
            'name': 'Message Test',
            'slug': 'message-test',
            'is_active': True
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        # Check that success message is in context
        messages = list(response.context.get('messages', []))
        self.assertTrue(any('created successfully' in str(m) for m in messages))
    
    def test_category_delete_shows_success_message(self):
        """Test that category deletion shows success message"""
        category = Category.objects.create(name='To Delete', slug='to-delete')
        
        response = self.client.post(
            reverse('category-delete', kwargs={'pk': category.pk}),
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        messages = list(response.context.get('messages', []))
        self.assertTrue(any('deleted successfully' in str(m) for m in messages))
