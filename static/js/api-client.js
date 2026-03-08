/**
 * Budget Ndio Story - Enhanced API Client Service
 * Production-ready API client with proper security, error handling, and SEO integration
 * 
 * Features:
 * - CSRF token protection for all mutating requests
 * - Production URL configuration
 * - Comprehensive error handling
 * - Request/response interceptors
 * - Rate limiting awareness
 * - SEO-friendly meta tag management
 */

(function() {
    'use strict';

    // Configuration - Production URL
    const API_CONFIG = {
        // Use relative URLs for local development, absolute for production
        // The API will use the same origin as the current page
        baseUrl: '/api/v1',
        authUrl: '/api/auth',
        
        // Request timeout (ms)
        timeout: 30000,
        
        // Retry configuration
        retryAttempts: 3,
        retryDelay: 1000,
        
        // Rate limiting
        rateLimit: {
            maxRequests: 100,
            windowMs: 60000 // 1 minute
        }
    };

    // Internal state
    let requestCount = 0;
    let windowStartTime = Date.now();

    // Get base URL based on environment
    function getBaseUrl() {
        // Always use relative URLs for same-origin requests
        return '/api/v1';
    }

    function getAuthUrl() {
        // Always use relative URLs for same-origin requests
        return '/api/auth';
    }

    // Get CSRF token from cookie
    function getCSRFToken() {
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
    }

    // Check rate limit
    function checkRateLimit() {
        const now = Date.now();
        if (now - windowStartTime > API_CONFIG.rateLimit.windowMs) {
            requestCount = 0;
            windowStartTime = now;
        }
        
        if (requestCount >= API_CONFIG.rateLimit.maxRequests) {
            return false;
        }
        
        requestCount++;
        return true;
    }

    // Enhanced request with retry logic
    async function makeRequest(url, options = {}, retryCount = 0) {
        // Check rate limit
        if (!checkRateLimit()) {
            throw new Error('Rate limit exceeded. Please try again later.');
        }

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
                'Accept': 'application/json',
            },
            credentials: 'include', // Important for session-based auth
            mode: 'cors',
        };

        const config = { ...defaultOptions, ...options };
        
        // Add CSRF token for mutating methods
        if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(config.method)) {
            config.headers['X-CSRFToken'] = getCSRFToken();
        }

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.timeout);
            config.signal = controller.signal;

            const response = await fetch(url, config);
            clearTimeout(timeoutId);

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
                // Handle specific error codes
                if (response.status === 401) {
                    // Unauthorized - redirect to login
                    window.dispatchEvent(new CustomEvent('auth:unauthorized', { detail: data }));
                    throw new Error(data.detail || 'Authentication required');
                }
                if (response.status === 403) {
                    // Forbidden
                    throw new Error(data.detail || 'Access denied');
                }
                if (response.status === 429) {
                    // Rate limited - retry with backoff
                    if (retryCount < API_CONFIG.retryAttempts) {
                        await new Promise(r => setTimeout(r, API_CONFIG.retryDelay * (retryCount + 1)));
                        return makeRequest(url, options, retryCount + 1);
                    }
                    throw new Error('Too many requests. Please try again later.');
                }
                throw new Error(data.detail || data.message || 'An error occurred');
            }

            return { success: true, data, status: response.status };
        } catch (error) {
            // Retry on network errors
            if (error.name === 'AbortError' && retryCount < API_CONFIG.retryAttempts) {
                await new Promise(r => setTimeout(r, API_CONFIG.retryDelay));
                return makeRequest(url, options, retryCount + 1);
            }
            
            console.error('API Error:', error);
            return { 
                success: false, 
                error: error.message,
                isNetworkError: error.name === 'AbortError'
            };
        }
    }

    // Main API object
    const API = {
        // Get base URL
        getBaseUrl: getBaseUrl,
        
        // Check if user is authenticated
        isAuthenticated: function() {
            return getCSRFToken() !== null;
        },

        // Generic request methods
        request: function(endpoint, options = {}) {
            const url = `${getBaseUrl()}${endpoint}`;
            return makeRequest(url, options);
        },

        get: function(endpoint) {
            return this.request(endpoint, { method: 'GET' });
        },

        post: function(endpoint, data) {
            return this.request(endpoint, {
                method: 'POST',
                body: JSON.stringify(data),
            });
        },

        put: function(endpoint, data) {
            return this.request(endpoint, {
                method: 'PUT',
                body: JSON.stringify(data),
            });
        },

        patch: function(endpoint, data) {
            return this.request(endpoint, {
                method: 'PATCH',
                body: JSON.stringify(data),
            });
        },

        delete: function(endpoint) {
            return this.request(endpoint, { method: 'DELETE' });
        },
    };

    // Authentication API - Enhanced with better security
    const AuthAPI = {
        // Get CSRF token explicitly
        getCSRFToken: getCSRFToken,

        // Login user with proper CSRF protection
        login: async function(username, password) {
            // First, ensure we have a CSRF token
            const csrfToken = getCSRFToken();
            
            const response = await fetch(`${getAuthUrl()}/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken || '',
                },
                credentials: 'include',
                body: JSON.stringify({ username, password }),
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Login failed');
            }
            
            // Dispatch auth event
            window.dispatchEvent(new CustomEvent('auth:login', { detail: data }));
            
            return data;
        },

        // Logout user with CSRF protection
        logout: async function() {
            const csrfToken = getCSRFToken();
            
            const response = await fetch(`${getAuthUrl()}/logout/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken || '',
                },
                credentials: 'include',
            });
            
            // Dispatch auth event
            window.dispatchEvent(new CustomEvent('auth:logout', {}));
            
            return response.ok;
        },

        // Get current user
        getCurrentUser: async function() {
            const response = await fetch(`${getAuthUrl()}/user/`, {
                method: 'GET',
                credentials: 'include',
            });
            
            if (!response.ok) {
                if (response.status === 401) {
                    return null;
                }
                throw new Error('Failed to get user');
            }
            return await response.json();
        },

        // Check if user is logged in
        isLoggedIn: async function() {
            try {
                const user = await this.getCurrentUser();
                return user !== null;
            } catch {
                return false;
            }
        },

        // Register new user
        register: async function(userData) {
            const response = await fetch(`${getBaseUrl()}/accounts/users/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken() || '',
                },
                credentials: 'include',
                body: JSON.stringify(userData),
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Registration failed');
            }
            
            return data;
        },
    };

    // Content API
    const ContentAPI = {
        videos: {
            list: (params = {}) => API.get(`/content/videos/?${new URLSearchParams(params)}`),
            get: (id) => API.get(`/content/videos/${id}/`),
            create: (data) => API.post('/content/videos/', data),
            update: (id, data) => API.put(`/content/videos/${id}/`, data),
            patch: (id, data) => API.patch(`/content/videos/${id}/`, data),
            delete: (id) => API.delete(`/content/videos/${id}/`),
        },
        
        categories: {
            list: () => API.get('/content/categories/'),
            get: (id) => API.get(`/content/categories/${id}/`),
            create: (data) => API.post('/content/categories/', data),
            update: (id, data) => API.put(`/content/categories/${id}/`, data),
            delete: (id) => API.delete(`/content/categories/${id}/`),
        },
        
        posts: {
            list: (params = {}) => API.get(`/content/posts/?${new URLSearchParams(params)}`),
            get: (id) => API.get(`/content/posts/${id}/`),
            create: (data) => API.post('/content/posts/', data),
            update: (id, data) => API.put(`/content/posts/${id}/`, data),
            patch: (id, data) => API.patch(`/content/posts/${id}/`, data),
            delete: (id) => API.delete(`/content/posts/${id}/`),
        },
        
        playlists: {
            list: () => API.get('/content/playlists/'),
            get: (id) => API.get(`/content/playlists/${id}/`),
            create: (data) => API.post('/content/playlists/', data),
            update: (id, data) => API.put(`/content/playlists/${id}/`, data),
            delete: (id) => API.delete(`/content/playlists/${id}/`),
        },
        
        news: {
            list: (params = {}) => API.get(`/content/news/?${new URLSearchParams(params)}`),
            get: (id) => API.get(`/content/news/${id}/`),
            create: (data) => API.post('/content/news/', data),
            update: (id, data) => API.put(`/content/news/${id}/`, data),
            delete: (id) => API.delete(`/content/news/${id}/`),
        },
    };

    // Accounts API
    const AccountsAPI = {
        users: {
            list: (params = {}) => API.get(`/accounts/users/?${new URLSearchParams(params)}`),
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

    // Sponsors API
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

    // SEO Manager - Update meta tags dynamically
    const SEOManager = {
        // Update page title
        setTitle: function(title) {
            document.title = title;
            this.updateMeta('og:title', title);
            this.updateMeta('twitter:title', title);
        },

        // Update meta description
        setDescription: function(description) {
            this.updateMeta('description', description);
            this.updateMeta('og:description', description);
            this.updateMeta('twitter:description', description);
        },

        // Update meta tag
        updateMeta: function(name, content) {
            let meta;
            
            // Handle Open Graph and Twitter with 'property' attribute
            if (name.startsWith('og:') || name.startsWith('twitter:')) {
                meta = document.querySelector(`meta[property="${name}"]`);
            } else {
                meta = document.querySelector(`meta[name="${name}"]`);
            }
            
            if (meta) {
                meta.setAttribute('content', content);
            }
        },

        // Update canonical URL
        setCanonical: function(url) {
            let link = document.querySelector('link[rel="canonical"]');
            if (!link) {
                link = document.createElement('link');
                link.setAttribute('rel', 'canonical');
                document.head.appendChild(link);
            }
            link.setAttribute('href', url);
        },

        // Set structured data
        setStructuredData: function(data) {
            let script = document.querySelector('script[type="application/ld+json"]');
            if (!script) {
                script = document.createElement('script');
                script.setAttribute('type', 'application/ld+json');
                document.head.appendChild(script);
            }
            script.textContent = JSON.stringify(data);
        },

        // Update image for social sharing
        setSocialImage: function(url) {
            this.updateMeta('og:image', url);
            this.updateMeta('twitter:image', url);
        },
    };

    // UI Helpers - Enhanced with better UX
    const UI = {
        // Show loading spinner
        showLoading: function(elementId, options = {}) {
            const element = document.getElementById(elementId);
            if (!element) return;

            const { message = 'Loading...', size = 'md' } = options;
            const sizeClass = size === 'sm' ? 'h-8 w-8' : 'h-12 w-12';
            
            element.innerHTML = `
                <div class="flex flex-col items-center justify-center p-8">
                    <div class="animate-spin rounded-full ${sizeClass} border-b-2 border-blue-600"></div>
                    <p class="mt-4 text-gray-400">${message}</p>
                </div>
            `;
        },

        // Hide loading
        hideLoading: function(elementId) {
            const element = document.getElementById(elementId);
            if (element) {
                element.innerHTML = '';
            }
        },

        // Show toast notification - Enhanced
        showToast: function(message, options = {}) {
            const container = document.getElementById('toast-container');
            if (!container) {
                console.warn('Toast container not found');
                return;
            }

            const { type = 'info', duration = 5000, dismissible = true } = options;
            
            const icons = {
                success: 'check-circle',
                error: 'x-circle',
                warning: 'alert-triangle',
                info: 'info',
                loading: 'loader'
            };
            
            const colors = {
                success: 'bg-green-500/10 border-green-500/20 text-green-400',
                error: 'bg-red-500/10 border-red-500/20 text-red-400',
                warning: 'bg-yellow-500/10 border-yellow-500/20 text-yellow-400',
                info: 'bg-blue-600/10 border-blue-600/20 text-blue-400',
                loading: 'bg-gray-500/10 border-gray-500/20 text-gray-400'
            };
            
            const toast = document.createElement('div');
            toast.className = `flex items-center gap-3 p-4 rounded-xl shadow-lg animate-slide-in border ${colors[type] || colors.info}`;
            
            let closeButton = '';
            if (dismissible) {
                closeButton = `<button onclick="this.parentElement.remove()" class="ml-auto hover:opacity-70" aria-label="Dismiss">
                    <i data-lucide="x" class="w-4 h-4"></i>
                </button>`;
            }
            
            toast.innerHTML = `
                <i data-lucide="${icons[type]}" class="w-5 h-5 flex-shrink-0"></i>
                <span class="text-sm font-medium">${message}</span>
                ${closeButton}
            `;
            
            container.appendChild(toast);
            
            // Initialize icons if Lucide is available
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
            
            // Auto-remove after duration
            if (duration > 0) {
                setTimeout(() => {
                    if (toast.parentElement) {
                        toast.remove();
                    }
                }, duration);
            }
            
            return toast;
        },

        // Show confirmation dialog
        confirm: function(message, options = {}) {
            const { title = 'Confirm', confirmText = 'Confirm', cancelText = 'Cancel', type = 'warning' } = options;
            
            return new Promise((resolve) => {
                const modal = document.createElement('div');
                modal.className = 'fixed inset-0 z-50 flex items-center justify-center p-4';
                modal.innerHTML = `
                    <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" onclick="resolve(false)"></div>
                    <div class="relative bg-gray-900 border border-gray-700 rounded-2xl p-6 max-w-md w-full shadow-2xl animate-fade-in">
                        <h3 class="text-lg font-semibold mb-2">${title}</h3>
                        <p class="text-gray-400 mb-6">${message}</p>
                        <div class="flex gap-3 justify-end">
                            <button class="cancel-btn px-4 py-2 rounded-lg border border-gray-600 hover:bg-gray-800 transition-colors">
                                ${cancelText}
                            </button>
                            <button class="confirm-btn px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 transition-colors">
                                ${confirmText}
                            </button>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(modal);
                
                modal.querySelector('.cancel-btn').onclick = () => {
                    modal.remove();
                    resolve(false);
                };
                
                modal.querySelector('.confirm-btn').onclick = () => {
                    modal.remove();
                    resolve(true);
                };
            });
        },

        // Format date
        formatDate: function(dateString, options = {}) {
            if (!dateString) return '-';
            
            const date = new Date(dateString);
            const { format = 'short', locale = 'en-KE' } = options;
            
            if (format === 'full') {
                return date.toLocaleDateString(locale, { 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                });
            }
            
            return date.toLocaleDateString(locale, { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric' 
            });
        },

        // Format currency
        formatCurrency: function(amount, currency = 'KES') {
            if (!amount && amount !== 0) return '-';
            return new Intl.NumberFormat('en-KE', {
                style: 'currency',
                currency: currency,
                minimumFractionDigits: 0,
                maximumFractionDigits: 0,
            }).format(amount);
        },

        // Validate form data
        validateForm: function(formData, rules) {
            const errors = {};
            
            for (const [field, rule] of Object.entries(rules)) {
                const value = formData.get(field);
                
                if (rule.required && !value) {
                    errors[field] = `${field.charAt(0).toUpperCase() + field.slice(1)} is required`;
                    continue;
                }
                
                if (value) {
                    if (rule.minLength && value.length < rule.minLength) {
                        errors[field] = `${field} must be at least ${rule.minLength} characters`;
                    }
                    
                    if (rule.maxLength && value.length > rule.maxLength) {
                        errors[field] = `${field} must be at most ${rule.maxLength} characters`;
                    }
                    
                    if (rule.pattern && !rule.pattern.test(value)) {
                        errors[field] = rule.message || `${field} is invalid`;
                    }
                    
                    if (rule.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
                        errors[field] = 'Please enter a valid email address';
                    }
                }
            }
            
            return {
                isValid: Object.keys(errors).length === 0,
                errors,
            };
        },

        // Debounce utility
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        // Show inline validation error
        showFieldError: function(fieldId, message) {
            const field = document.getElementById(fieldId);
            if (!field) return;
            
            // Remove existing error
            const existingError = field.parentElement.querySelector('.field-error');
            if (existingError) existingError.remove();
            
            // Add error class
            field.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
            
            // Add error message
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error text-red-500 text-sm mt-1';
            errorDiv.textContent = message;
            field.parentElement.appendChild(errorDiv);
        },

        // Clear field error
        clearFieldError: function(fieldId) {
            const field = document.getElementById(fieldId);
            if (!field) return;
            
            field.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
            
            const errorDiv = field.parentElement.querySelector('.field-error');
            if (errorDiv) errorDiv.remove();
        },
    };

    // Form Handler - Simplified form submission with validation
    const FormHandler = {
        // Handle form submission
        handleSubmit: async function(formId, options = {}) {
            const form = document.getElementById(formId);
            if (!form) {
                console.error('Form not found:', formId);
                return;
            }

            const { 
                onSuccess, 
                onError, 
                validate = true,
                rules = {},
                resetOnSuccess = true 
            } = options;

            form.addEventListener('submit', async (e) => {
                e.preventDefault();

                const formData = new FormData(form);
                
                // Validate if rules provided
                if (validate && Object.keys(rules).length > 0) {
                    const validation = UI.validateForm(formData, rules);
                    if (!validation.isValid) {
                        // Show errors
                        for (const [field, error] of Object.entries(validation.errors)) {
                            UI.showFieldError(field, error);
                        }
                        return;
                    }
                }

                // Show loading state
                const submitBtn = form.querySelector('button[type="submit"]');
                const originalText = submitBtn?.textContent;
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="animate-spin mr-2">⟳</span> Processing...';
                }

                try {
                    const data = Object.fromEntries(formData);
                    const result = await API.post(options.endpoint || '', data);
                    
                    if (result.success) {
                        if (onSuccess) await onSuccess(result.data);
                        if (resetOnSuccess) form.reset();
                    } else {
                        if (onError) await onError(result.error);
                        UI.showToast(result.error || 'An error occurred', { type: 'error' });
                    }
                } catch (error) {
                    if (onError) await onError(error.message);
                    UI.showToast(error.message || 'An error occurred', { type: 'error' });
                } finally {
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.textContent = originalText;
                    }
                }
            });
        },
    };

    // Export for use in templates
    window.API = API;
    window.AuthAPI = AuthAPI;
    window.ContentAPI = ContentAPI;
    window.AccountsAPI = AccountsAPI;
    window.NewsletterAPI = NewsletterAPI;
    window.SponsorsAPI = SponsorsAPI;
    window.SEOManager = SEOManager;
    window.UI = UI;
    window.FormHandler = FormHandler;
    
    // Export configuration for external use
    window.API_CONFIG = API_CONFIG;

    // Initialize auth state check on page load
    document.addEventListener('DOMContentLoaded', async function() {
        console.log('API Client initialized');
        
        // Check auth state
        try {
            const user = await AuthAPI.getCurrentUser();
            if (user) {
                window.dispatchEvent(new CustomEvent('auth:ready', { detail: user }));
            }
        } catch (error) {
            console.log('Auth check failed:', error.message);
        }
    });

})();
