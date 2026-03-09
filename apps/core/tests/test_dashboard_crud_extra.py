"""
Additional tests for Accounts and Sponsors CRUD operations.
"""
from django.test import TestCase, Client
from django.urls import reverse

from apps.accounts.models import User, DonorProfile, SponsorProfile, ConsortiumPartner
from apps.sponsors.models import Donation, SponsorshipDeliverable


class UserListTestCase(TestCase):
    """Test User list view"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        # Create regular users
        User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='pass123',
            role='editor'
        )
        User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='pass123',
            role='viewer'
        )
    
    def test_user_list_view(self):
        """Test user list displays correctly"""
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)
        # Should show the admin user and the two regular users
        self.assertContains(response, 'admin@test.com')
        self.assertContains(response, 'user1@test.com')


class DonorListTestCase(TestCase):
    """Test Donor list view"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        # Create donor profiles
        user1 = User.objects.create_user(
            username='donor1',
            email='donor1@test.com',
            password='pass123'
        )
        user2 = User.objects.create_user(
            username='donor2',
            email='donor2@test.com',
            password='pass123'
        )
        
        DonorProfile.objects.create(user=user1, donor_type='individual', total_donated=100.00)
        DonorProfile.objects.create(user=user2, donor_type='corporate', total_donated=500.00)
    
    def test_donor_list_view(self):
        """Test donor list displays correctly"""
        response = self.client.get(reverse('donor-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'donor1@test.com')
        self.assertContains(response, 'donor2@test.com')


class SponsorListTestCase(TestCase):
    """Test Sponsor list view"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        # Create sponsor profiles
        user1 = User.objects.create_user(
            username='sponsor1',
            email='sponsor1@test.com',
            password='pass123'
        )
        user2 = User.objects.create_user(
            username='sponsor2',
            email='sponsor2@test.com',
            password='pass123'
        )
        
        SponsorProfile.objects.create(
            user=user1,
            company_name='Company 1',
            level='gold',
            contract_value=10000.00,
            contract_start='2024-01-01',
            contract_end='2024-12-31'
        )
        SponsorProfile.objects.create(
            user=user2,
            company_name='Company 2',
            level='silver',
            contract_value=5000.00,
            contract_start='2024-01-01',
            contract_end='2024-12-31'
        )
    
    def test_sponsor_list_view(self):
        """Test sponsor list displays correctly"""
        response = self.client.get(reverse('sponsor-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Company 1')
        self.assertContains(response, 'Company 2')


class PartnerListTestCase(TestCase):
    """Test Consortium Partner list view"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        # Create partners
        ConsortiumPartner.objects.create(
            name='Partner 1',
            slug='partner-1',
            website='https://partner1.com'
        )
        ConsortiumPartner.objects.create(
            name='Partner 2',
            slug='partner-2',
            website='https://partner2.com'
        )
    
    def test_partner_list_view(self):
        """Test partner list displays correctly"""
        response = self.client.get(reverse('partner-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Partner 1')
        self.assertContains(response, 'Partner 2')


class DeliverableCRUDTestCase(TestCase):
    """Test Sponsorship Deliverable CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        # Create sponsor profile
        sponsor_user = User.objects.create_user(
            username='sponsor',
            email='sponsor@test.com',
            password='pass123'
        )
        self.sponsor = SponsorProfile.objects.create(
            user=sponsor_user,
            company_name='Test Company',
            level='gold',
            contract_value=10000.00,
            contract_start='2024-01-01',
            contract_end='2024-12-31'
        )
        
        from datetime import date
        self.deliverable = SponsorshipDeliverable.objects.create(
            sponsor=self.sponsor,
            deliverable_type='logo_display',
            description='Display logo on homepage',
            due_date=date(2024, 6, 30)
        )
    
    def test_deliverable_list_view(self):
        """Test deliverable list displays correctly"""
        response = self.client.get(reverse('deliverable-list'))
        self.assertEqual(response.status_code, 200)
    
    def test_deliverable_create_view(self):
        """Test deliverable creation"""
        from datetime import date
        response = self.client.post(reverse('deliverable-create'), {
            'sponsor': self.sponsor.pk,
            'deliverable_type': 'dedicated_content',
            'description': 'Create dedicated content',
            'due_date': '2024-12-31'
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify deliverable was created
        self.assertTrue(SponsorshipDeliverable.objects.filter(
            deliverable_type='dedicated_content'
        ).exists())
    
    def test_deliverable_update_view(self):
        """Test deliverable update"""
        response = self.client.post(
            reverse('deliverable-update', kwargs={'pk': self.deliverable.pk}),
            {
                'sponsor': self.sponsor.pk,
                'deliverable_type': 'logo_display',
                'description': 'Updated description',
                'due_date': '2024-06-30',
                'status': 'completed'
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify deliverable was updated
        self.deliverable.refresh_from_db()
        self.assertEqual(self.deliverable.description, 'Updated description')
        self.assertEqual(self.deliverable.status, 'completed')
    
    def test_deliverable_delete_view(self):
        """Test deliverable deletion"""
        deliverable_id = self.deliverable.pk
        response = self.client.post(reverse('deliverable-delete', kwargs={'pk': deliverable_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify deliverable was deleted
        self.assertFalse(SponsorshipDeliverable.objects.filter(pk=deliverable_id).exists())


class NewsItemCRUDTestCase(TestCase):
    """Test NewsItem CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        self.newsitem = NewsItem.objects.create(
            title='Test News',
            slug='test-news',
            content='Test content for news item'
        )
    
    def test_newsitem_list_view(self):
        """Test news item list displays correctly"""
        response = self.client.get(reverse('newsitem-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test News')
    
    def test_newsitem_create_view(self):
        """Test news item creation"""
        response = self.client.post(reverse('newsitem-create'), {
            'title': 'New News',
            'slug': 'new-news',
            'content': 'New content'
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify news item was created
        self.assertTrue(NewsItem.objects.filter(slug='new-news').exists())
    
    def test_newsitem_update_view(self):
        """Test news item update"""
        response = self.client.post(
            reverse('newsitem-update', kwargs={'pk': self.newsitem.pk}),
            {
                'title': 'Updated News',
                'slug': 'test-news',
                'content': 'Updated content',
                'is_breaking': True
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify news item was updated
        self.newsitem.refresh_from_db()
        self.assertEqual(self.newsitem.title, 'Updated News')
        self.assertTrue(self.newsitem.is_breaking)
    
    def test_newsitem_delete_view(self):
        """Test news item deletion"""
        newsitem_id = self.newsitem.pk
        response = self.client.post(reverse('newsitem-delete', kwargs={'pk': newsitem_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify news item was deleted
        self.assertFalse(NewsItem.objects.filter(pk=newsitem_id).exists())


class MenuItemCRUDTestCase(TestCase):
    """Test MenuItem CRUD operations"""
    
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
        
        self.menuitem = MenuItem.objects.create(
            menu=self.menu,
            title='Test Item',
            link_type='url',
            url='/test/',
            order=1
        )
    
    def test_menuitem_list_view(self):
        """Test menu item list displays correctly"""
        response = self.client.get(reverse('menuitem-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
    
    def test_menuitem_create_view(self):
        """Test menu item creation"""
        response = self.client.post(reverse('menuitem-create'), {
            'menu': self.menu.pk,
            'title': 'New Item',
            'link_type': 'url',
            'url': '/new/',
            'order': 2
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify menu item was created
        self.assertTrue(MenuItem.objects.filter(title='New Item').exists())
    
    def test_menuitem_update_view(self):
        """Test menu item update"""
        response = self.client.post(
            reverse('menuitem-update', kwargs={'pk': self.menuitem.pk}),
            {
                'menu': self.menu.pk,
                'title': 'Updated Item',
                'link_type': 'url',
                'url': '/updated/',
                'order': 1
            }
        )
        self.assertIn(response.status_code, [302, 200])
        
        # Verify menu item was updated
        self.menuitem.refresh_from_db()
        self.assertEqual(self.menuitem.title, 'Updated Item')
    
    def test_menuitem_delete_view(self):
        """Test menu item deletion"""
        menuitem_id = self.menuitem.pk
        response = self.client.post(reverse('menuitem-delete', kwargs={'pk': menuitem_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify menu item was deleted
        self.assertFalse(MenuItem.objects.filter(pk=menuitem_id).exists())


class AssetCRUDTestCase(TestCase):
    """Test Sponsor Asset CRUD operations"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='adminpass123')
        
        # Create sponsor profile
        sponsor_user = User.objects.create_user(
            username='sponsor',
            email='sponsor@test.com',
            password='pass123'
        )
        self.sponsor = SponsorProfile.objects.create(
            user=sponsor_user,
            company_name='Test Company',
            level='gold',
            contract_value=10000.00,
            contract_start='2024-01-01',
            contract_end='2024-12-31'
        )
        
        # Create a simple test file
        test_file = SimpleUploadedFile(
            "test_logo.png",
            b"file_content",
            content_type="image/png"
        )
        
        self.asset = SponsorAsset.objects.create(
            sponsor=self.sponsor,
            name='Test Logo',
            file=test_file,
            asset_type='logo'
        )
    
    def test_asset_list_view(self):
        """Test asset list displays correctly"""
        response = self.client.get(reverse('asset-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Logo')
    
    def test_asset_create_view(self):
        """Test asset creation"""
        test_file = SimpleUploadedFile(
            "new_logo.png",
            b"file_content",
            content_type="image/png"
        )
        
        response = self.client.post(reverse('asset-create'), {
            'sponsor': self.sponsor.pk,
            'name': 'New Logo',
            'file': test_file,
            'asset_type': 'logo'
        })
        self.assertIn(response.status_code, [302, 200])
        
        # Verify asset was created
        self.assertTrue(SponsorAsset.objects.filter(name='New Logo').exists())
    
    def test_asset_delete_view(self):
        """Test asset deletion"""
        asset_id = self.asset.pk
        response = self.client.post(reverse('asset-delete', kwargs={'pk': asset_id}))
        self.assertEqual(response.status_code, 302)
        
        # Verify asset was deleted
        self.assertFalse(SponsorAsset.objects.filter(pk=asset_id).exists())
