/**
 * Budget Ndio Story - API Client Service
 * Provides unified interface for interacting with Django REST API endpoints
 */

const API = {
    baseUrl: '/api/v1',
    authUrl: '/api/auth',
    
    // Get CSRF token from cookie
    getCSRFToken: function() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    // Make API request with proper headers and error handling
    request: async function(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken(),
            },
            credentials: 'include',
        };

        const config = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, config);
            
            // Handle non-JSON responses
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return { success: true, data: await response.text() };
            }
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || data.message || 'An error occurred');
            }
            
            return { success: true, data };
        } catch (error) {
            console.error('API Error:', error);
            return { success: false, error: error.message };
        }
    },

    // GET request
    get: function(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },

    // POST request
    post: function(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    // PUT request
    put: function(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    // PATCH request
    patch: function(endpoint, data) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    },

    // DELETE request
    delete: function(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    },
};

// Authentication API
const AuthAPI = {
    // Login user
    login: async function(username, password) {
        const response = await fetch('/api/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ username, password }),
        });
        
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Login failed');
        }
        return data;
    },

    // Logout user
    logout: async function() {
        const response = await fetch('/api/auth/logout/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': API.getCSRFToken(),
            },
            credentials: 'include',
        });
        
        return response.ok;
    },

    // Get current user
    getCurrentUser: async function() {
        const response = await fetch('/api/auth/user/', {
            method: 'GET',
            credentials: 'include',
        });
        
        if (!response.ok) {
            return null;
        }
        return await response.json();
    },
};

// Content API - Videos, Posts, Categories, etc.
const ContentAPI = {
    // Videos
    videos: {
        list: () => API.get('/content/videos/'),
        get: (id) => API.get(`/content/videos/${id}/`),
        create: (data) => API.post('/content/videos/', data),
        update: (id, data) => API.put(`/content/videos/${id}/`, data),
        patch: (id, data) => API.patch(`/content/videos/${id}/`, data),
        delete: (id) => API.delete(`/content/videos/${id}/`),
    },
    
    // Categories
    categories: {
        list: () => API.get('/content/categories/'),
        get: (id) => API.get(`/content/categories/${id}/`),
        create: (data) => API.post('/content/categories/', data),
        update: (id, data) => API.put(`/content/categories/${id}/`, data),
        delete: (id) => API.delete(`/content/categories/${id}/`),
    },
    
    // Blog Posts
    posts: {
        list: () => API.get('/content/posts/'),
        get: (id) => API.get(`/content/posts/${id}/`),
        create: (data) => API.post('/content/posts/', data),
        update: (id, data) => API.put(`/content/posts/${id}/`, data),
        patch: (id, data) => API.patch(`/content/posts/${id}/`, data),
        delete: (id) => API.delete(`/content/posts/${id}/`),
    },
    
    // Playlists
    playlists: {
        list: () => API.get('/content/playlists/'),
        get: (id) => API.get(`/content/playlists/${id}/`),
        create: (data) => API.post('/content/playlists/', data),
        update: (id, data) => API.put(`/content/playlists/${id}/`, data),
        delete: (id) => API.delete(`/content/playlists/${id}/`),
    },
    
    // News
    news: {
        list: () => API.get('/content/news/'),
        get: (id) => API.get(`/content/news/${id}/`),
        create: (data) => API.post('/content/news/', data),
        update: (id, data) => API.put(`/content/news/${id}/`, data),
        delete: (id) => API.delete(`/content/news/${id}/`),
    },
};

// Accounts API - Users, Donors, Sponsors
const AccountsAPI = {
    users: {
        list: () => API.get('/accounts/users/'),
        get: (id) => API.get(`/accounts/users/${id}/`),
        create: (data) => API.post('/accounts/users/', data),
        update: (id, data) => API.put(`/accounts/users/${id}/`, data),
        delete: (id) => API.delete(`/accounts/users/${id}/`),
    },
    
    donors: {
        list: () => API.get('/accounts/donors/'),
        get: (id) => API.get(`/accounts/donors/${id}/`),
        create: (data) => API.post('/accounts/donors/', data),
        update: (id, data) => API.put(`/accounts/donors/${id}/`, data),
        delete: (id) => API.delete(`/accounts/donors/${id}/`),
    },
    
    sponsors: {
        list: () => API.get('/accounts/sponsors/'),
        get: (id) => API.get(`/accounts/sponsors/${id}/`),
        create: (data) => API.post('/accounts/sponsors/', data),
        update: (id, data) => API.put(`/accounts/sponsors/${id}/`, data),
        delete: (id) => API.delete(`/accounts/sponsors/${id}/`),
    },
    
    partners: {
        list: () => API.get('/accounts/partners/'),
        get: (id) => API.get(`/accounts/partners/${id}/`),
        create: (data) => API.post('/accounts/partners/', data),
        delete: (id) => API.delete(`/accounts/partners/${id}/`),
    },
};

// Newsletter API
const NewsletterAPI = {
    subscribers: {
        list: () => API.get('/newsletter/subscribers/'),
        get: (id) => API.get(`/newsletter/subscribers/${id}/`),
        create: (data) => API.post('/newsletter/subscribers/', data),
        update: (id, data) => API.put(`/newsletter/subscribers/${id}/`, data),
        delete: (id) => API.delete(`/newsletter/subscribers/${id}/`),
    },
    
    campaigns: {
        list: () => API.get('/newsletter/campaigns/'),
        get: (id) => API.get(`/newsletter/campaigns/${id}/`),
        create: (data) => API.post('/newsletter/campaigns/', data),
        update: (id, data) => API.put(`/newsletter/campaigns/${id}/`, data),
        delete: (id) => API.delete(`/newsletter/campaigns/${id}/`),
    },
};

// Sponsors API - Donations, Deliverables, Assets
const SponsorsAPI = {
    donations: {
        list: () => API.get('/sponsors/donations/'),
        get: (id) => API.get(`/sponsors/donations/${id}/`),
        create: (data) => API.post('/sponsors/donations/', data),
        update: (id, data) => API.put(`/sponsors/donations/${id}/`, data),
        delete: (id) => API.delete(`/sponsors/donations/${id}/`),
    },
    
    deliverables: {
        list: () => API.get('/sponsors/deliverables/'),
        get: (id) => API.get(`/sponsors/deliverables/${id}/`),
        create: (data) => API.post('/sponsors/deliverables/', data),
        update: (id, data) => API.put(`/sponsors/deliverables/${id}/`, data),
        delete: (id) => API.delete(`/sponsors/deliverables/${id}/`),
    },
    
    assets: {
        list: () => API.get('/sponsors/assets/'),
        get: (id) => API.get(`/sponsors/assets/${id}/`),
        create: (data) => API.post('/sponsors/assets/', data),
        delete: (id) => API.delete(`/sponsors/assets/${id}/`),
    },
};

// UI Helpers
const UI = {
    // Show loading spinner
    showLoading: function(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = '<div class="flex items-center justify-center p-8"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>';
        }
    },

    // Show toast notification
    showToast: function(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        const icons = {
            success: 'check-circle',
            error: 'x-circle',
            warning: 'alert-triangle',
            info: 'info'
        };
        
        toast.className = `flex items-center gap-3 p-4 rounded-xl shadow-lg animate-slide-in ${
            type === 'success' ? 'bg-green-500/10 border border-green-500/20 text-green-400' :
            type === 'error' ? 'bg-red-500/10 border border-red-500/20 text-red-400' :
            type === 'warning' ? 'bg-yellow-500/10 border border-yellow-500/20 text-yellow-400' :
            'bg-blue-600/10 border border-blue-600/20 text-blue-400'
        }`;
        
        toast.innerHTML = `
            <i data-lucide="${icons[type]}" class="w-5 h-5 flex-shrink-0"></i>
            <span class="text-sm font-medium">${message}</span>
            <button onclick="this.parentElement.remove()" class="ml-auto hover:opacity-70">
                <i data-lucide="x" class="w-4 h-4"></i>
            </button>
        `;
        
        container.appendChild(toast);
        lucide.createIcons();
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            toast.remove();
        }, 5000);
    },

    // Show confirmation dialog
    confirm: function(message) {
        return confirm(message);
    },

    // Render table row
    renderTableRow: function(item, columns, actions) {
        let html = '<tr class="hover:bg-gray-50">';
        
        columns.forEach(col => {
            html += `<td class="px-6 py-4">${item[col.key] || '-'}</td>`;
        });
        
        html += '<td class="px-6 py-4"><div class="flex items-center gap-2">';
        
        actions.forEach(action => {
            const icon = action.icon || 'edit';
            const className = action.className || 'text-gray-500 hover:text-blue-600';
            const onclick = action.onclick ? `onclick="${action.onclick}"` : '';
            html += `<button ${onclick} class="p-2 ${className} transition-colors" title="${action.title}">
                <i data-lucide="${icon}" class="w-5 h-5"></i>
            </button>`;
        });
        
        html += '</div></td></tr>';
        
        return html;
    },

    // Format date
    formatDate: function(dateString) {
        if (!dateString) return '-';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    },

    // Format currency
    formatCurrency: function(amount, currency = 'KES') {
        if (!amount) return '-';
        return new Intl.NumberFormat('en-KE', {
            style: 'currency',
            currency: currency,
        }).format(amount);
    },

    // Validate form data
    validateForm: function(formData, rules) {
        const errors = {};
        
        for (const [field, rule] of Object.entries(rules)) {
            const value = formData.get(field);
            
            if (rule.required && !value) {
                errors[field] = `${field} is required`;
            }
            
            if (rule.minLength && value && value.length < rule.minLength) {
                errors[field] = `${field} must be at least ${rule.minLength} characters`;
            }
            
            if (rule.pattern && value && !rule.pattern.test(value)) {
                errors[field] = rule.message || `${field} is invalid`;
            }
        }
        
        return {
            isValid: Object.keys(errors).length === 0,
            errors,
        };
    },
};

// Export for use in templates
window.API = API;
window.AuthAPI = AuthAPI;
window.ContentAPI = ContentAPI;
window.AccountsAPI = AccountsAPI;
window.NewsletterAPI = NewsletterAPI;
window.SponsorsAPI = SponsorsAPI;
window.UI = UI;