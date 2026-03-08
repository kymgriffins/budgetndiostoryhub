from django import forms
from django.utils.text import slugify
from .models import Page, Menu, MenuItem, SiteSetting, Widget, MediaLibrary


class PageForm(forms.ModelForm):
    """Form for creating/editing CMS pages"""
    
    class Meta:
        model = Page
        fields = [
            'title', 'slug', 'subtitle', 'content', 'content_html',
            'template', 'meta_title', 'meta_description', 'og_image',
            'featured_image', 'video_url', 'status', 'is_featured',
            'show_in_nav', 'nav_order', 'show_sidebar', 'show_comments',
            'full_width', 'background_color', 'background_image', 'author'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Page title'}),
            'slug': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'URL slug'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Subtitle'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea w-full', 'rows': 10, 'placeholder': 'Page content (Markdown)'}),
            'content_html': forms.Textarea(attrs={'class': 'form-textarea w-full', 'rows': 10, 'placeholder': 'Page content (HTML)'}),
            'template': forms.Select(attrs={'class': 'form-select'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-input w-full', 'maxlength': 70, 'placeholder': 'SEO title (max 70 chars)'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-input w-full', 'maxlength': 160, 'placeholder': 'SEO description (max 160 chars)'}),
            'og_image': forms.ClearableFileInput(attrs={'class': 'form-file'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-file'}),
            'video_url': forms.URLInput(attrs={'class': 'form-input w-full', 'placeholder': 'https://...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'nav_order': forms.NumberInput(attrs={'class': 'form-input w-full', 'min': 0}),
            'background_color': forms.TextInput(attrs={'class': 'form-input w-full', 'type': 'color'}),
            'background_image': forms.ClearableFileInput(attrs={'class': 'form-file'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug and self.cleaned_data.get('title'):
            slug = slugify(self.cleaned_data['title'])[:50]
        
        # Check for duplicate slugs excluding current instance
        queryset = Page.objects.filter(slug=slug)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError("A page with this slug already exists.")
        
        return slug


class MenuForm(forms.ModelForm):
    """Form for creating/editing menus"""
    
    class Meta:
        model = Menu
        fields = ['name', 'slug', 'description', 'location', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Menu name'}),
            'slug': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'URL-friendly slug'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea w-full', 'rows': 3, 'placeholder': 'Description'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
        }


class MenuItemForm(forms.ModelForm):
    """Form for creating/editing menu items"""
    
    class Meta:
        model = MenuItem
        fields = [
            'menu', 'parent', 'title', 'link_type', 'page', 'url', 'category',
            'icon', 'css_class', 'target_new_tab', 'order', 'is_active'
        ]
        widgets = {
            'menu': forms.Select(attrs={'class': 'form-select'}),
            'parent': forms.Select(attrs={'class': 'form-select'}, choices=[('', '---------')]),
            'title': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Menu item title'}),
            'link_type': forms.Select(attrs={'class': 'form-select'}),
            'page': forms.Select(attrs={'class': 'form-select'}, choices=[('', '---------')]),
            'url': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'https://...'}),
            'category': forms.Select(attrs={'class': 'form-select'}, choices=[('', '---------')]),
            'icon': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Icon class (e.g., ph ph-home)'}),
            'css_class': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'CSS classes'}),
            'order': forms.NumberInput(attrs={'class': 'form-input w-full', 'min': 0}),
        }


class SiteSettingForm(forms.ModelForm):
    """Form for creating/editing site settings"""
    
    class Meta:
        model = SiteSetting
        fields = ['key', 'value', 'value_type', 'category', 'description', 'is_public']
        widgets = {
            'key': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Setting key (e.g., site_name)'}),
            'value': forms.Textarea(attrs={'class': 'form-textarea w-full', 'rows': 3, 'placeholder': 'Setting value'}),
            'value_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea w-full', 'rows': 2, 'placeholder': 'Description for admins'}),
        }
    
    def clean_key(self):
        key = self.cleaned_data.get('key')
        # Check for duplicate keys excluding current instance
        queryset = SiteSetting.objects.filter(key=key)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError("A setting with this key already exists.")
        
        return key


class WidgetForm(forms.ModelForm):
    """Form for creating/editing widgets"""
    
    class Meta:
        model = Widget
        fields = ['name', 'widget_type', 'title', 'content', 'settings', 'css_class', 'is_active', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Widget name'}),
            'widget_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Widget title'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea w-full', 'rows': 5, 'placeholder': 'Widget content'}),
            'settings': forms.Textarea(attrs={'class': 'form-textarea w-full', 'rows': 3, 'placeholder': '{"key": "value"}'}),
            'css_class': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'CSS classes'}),
            'order': forms.NumberInput(attrs={'class': 'form-input w-full', 'min': 0}),
        }


class MediaLibraryForm(forms.ModelForm):
    """Form for uploading media files"""
    
    class Meta:
        model = MediaLibrary
        fields = ['file', 'filename', 'media_type', 'title', 'alt_text', 'caption', 'folder', 'tags', 'uploaded_by']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-file'}),
            'filename': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Filename'}),
            'media_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Title'}),
            'alt_text': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Alt text for images'}),
            'caption': forms.Textarea(attrs={'class': 'form-textarea w-full', 'rows': 2, 'placeholder': 'Caption'}),
            'folder': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Folder path'}),
            'tags': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Comma-separated tags'}),
            'uploaded_by': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            if isinstance(tags, str):
                return [t.strip() for t in tags.split(',') if t.strip()]
        return []
