/**
 * Budget Ndio Story - Frontend Application
 * Production-ready JavaScript with ES6+ features
 * 
 * Features:
 * - Client-side routing
 * - Form validation
 * - UI components and utilities
 * - Authentication management
 * - API integration patterns
 * - Error handling
 */

(function() {
    'use strict';

    // ===========================================
    // CONFIGURATION
    // ===========================================
    
    const AppConfig = {
        // API Configuration
        apiBaseUrl: '/api/v1',
        authUrl: '/api/auth',
        
        // App Configuration
        appName: 'Budget Ndio Story',
        appVersion: '1.0.0',
        
        // Routing
        defaultRoute: '/',
        routes: {
            '/': 'home',
            '/home': 'home',
            '/dashboard': 'dashboard',
            '/login': 'login',
            '/register': 'register',
            '/logout': 'logout',
            '/password-reset': 'passwordReset',
            '/profile': 'profile',
            '/settings': 'settings',
            '/content': 'content',
            '/content/videos': 'videos',
            '/content/blog': 'blog',
            '/content/news': 'news',
            '/newsletter': 'newsletter',
            '/sponsors': 'sponsors',
        },
        
        // Pagination
        defaultPageSize: 10,
        pageSizeOptions: [10, 25, 50, 100],
        
        // Storage Keys
        storageKeys: {
            user: 'app_user',
            token: 'app_token',
            theme: 'app_theme',
            sidebar: 'app_sidebar_state',
        },
        
        // Timeouts
        requestTimeout: 30000,
        toastDuration: 5000,
    };

    // ===========================================
    // UTILITY FUNCTIONS
    // ===========================================
    
    const Utils = {
        /**
         * Generate unique ID
         */
        generateId: function() {
            return 'id_' + Math.random().toString(36).substr(2, 9);
        },
        
        /**
         * Debounce function
         */
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
        
        /**
         * Throttle function
         */
        throttle: function(func, limit) {
            let inThrottle;
            return function(...args) {
                if (!inThrottle) {
                    func.apply(this, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },
        
        /**
         * Format date
         */
        formatDate: function(date, format = 'short') {
            const d = new Date(date);
            const options = format === 'long' 
                ? { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }
                : { year: 'numeric', month: 'short', day: 'numeric' };
            return d.toLocaleDateString('en-US', options);
        },
        
        /**
         * Format relative time
         */
        formatRelativeTime: function(date) {
            const now = new Date();
            const past = new Date(date);
            const diffMs = now - past;
            const diffSecs = Math.floor(diffMs / 1000);
            const diffMins = Math.floor(diffSecs / 60);
            const diffHours = Math.floor(diffMins / 60);
            const diffDays = Math.floor(diffHours / 24);
            
            if (diffSecs < 60) return 'just now';
            if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
            if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
            if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
            return Utils.formatDate(date);
        },
        
        /**
         * Format number with commas
         */
        formatNumber: function(num) {
            return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        },
        
        /**
         * Format currency
         */
        formatCurrency: function(amount, currency = 'KES') {
            return new Intl.NumberFormat('en-KE', {
                style: 'currency',
                currency: currency,
                minimumFractionDigits: 0,
            }).format(amount);
        },
        
        /**
         * Truncate text
         */
        truncateText: function(text, length = 100, suffix = '...') {
            if (text.length <= length) return text;
            return text.substring(0, length).trim() + suffix;
        },
        
        /**
         * Slugify text
         */
        slugify: function(text) {
            return text
                .toLowerCase()
                .trim()
                .replace(/[^\w\s-]/g, '')
                .replace(/[\s_-]+/g, '-')
                .replace(/^-+|-+$/g, '');
        },
        
        /**
         * Parse URL query parameters
         */
        parseQueryParams: function() {
            const params = new URLSearchParams(window.location.search);
            const result = {};
            for (const [key, value] of params) {
                result[key] = value;
            }
            return result;
        },
        
        /**
         * Build URL with query parameters
         */
        buildUrl: function(path, params = {}) {
            const url = new URL(path, window.location.origin);
            Object.keys(params).forEach(key => {
                if (params[key] !== null && params[key] !== undefined) {
                    url.searchParams.append(key, params[key]);
                }
            });
            return url.toString();
        },
        
        /**
         * Get nested property from object
         */
        getNestedValue: function(obj, path, defaultValue = null) {
            return path.split('.').reduce((acc, part) => acc && acc[part], obj) || defaultValue;
        },
        
        /**
         * Deep clone object
         */
        deepClone: function(obj) {
            return JSON.parse(JSON.stringify(obj));
        },
        
        /**
         * Check if object is empty
         */
        isEmpty: function(obj) {
            if (obj == null) return true;
            if (Array.isArray(obj) || typeof obj === 'string') return obj.length === 0;
            return Object.keys(obj).length === 0;
        },
        
        /**
         * Capitalize first letter
         */
        capitalize: function(str) {
            return str.charAt(0).toUpperCase() + str.slice(1);
        },
        
        /**
         * Get initials from name
         */
        getInitials: function(name) {
            return name
                .split(' ')
                .map(word => word.charAt(0))
                .join('')
                .toUpperCase()
                .substring(0, 2);
        },
        
        /**
         * Copy text to clipboard
         */
        copyToClipboard: async function(text) {
            try {
                await navigator.clipboard.writeText(text);
                return true;
            } catch (err) {
                console.error('Failed to copy:', err);
                return false;
            }
        },
        
        /**
         * Download file
         */
        downloadFile: function(data, filename, mimeType = 'text/plain') {
            const blob = new Blob([data], { type: mimeType });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        },
        
        /**
         * Wait for element to exist
         */
        waitForElement: function(selector, timeout = 5000) {
            return new Promise((resolve, reject) => {
                const element = document.querySelector(selector);
                if (element) {
                    resolve(element);
                    return;
                }
                
                const observer = new MutationObserver(() => {
                    const element = document.querySelector(selector);
                    if (element) {
                        observer.disconnect();
                        resolve(element);
                    }
                });
                
                observer.observe(document.body, {
                    childList: true,
                    subtree: true,
                });
                
                setTimeout(() => {
                    observer.disconnect();
                    reject(new Error(`Element ${selector} not found within ${timeout}ms`));
                }, timeout);
            });
        },
    };

    // ===========================================
    // STORAGE UTILITIES
    // ===========================================
    
    const Storage = {
        /**
         * Get item from storage
         */
        get: function(key, defaultValue = null) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : defaultValue;
            } catch (e) {
                console.error('Storage get error:', e);
                return defaultValue;
            }
        },
        
        /**
         * Set item in storage
         */
        set: function(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
                return true;
            } catch (e) {
                console.error('Storage set error:', e);
                return false;
            }
        },
        
        /**
         * Remove item from storage
         */
        remove: function(key) {
            try {
                localStorage.removeItem(key);
                return true;
            } catch (e) {
                console.error('Storage remove error:', e);
                return false;
            }
        },
        
        /**
         * Clear all storage
         */
        clear: function() {
            try {
                localStorage.clear();
                return true;
            } catch (e) {
                console.error('Storage clear error:', e);
                return false;
            }
        },
        
        /**
         * Get session item
         */
        getSession: function(key, defaultValue = null) {
            try {
                const item = sessionStorage.getItem(key);
                return item ? JSON.parse(item) : defaultValue;
            } catch (e) {
                return defaultValue;
            }
        },
        
        /**
         * Set session item
         */
        setSession: function(key, value) {
            try {
                sessionStorage.setItem(key, JSON.stringify(value));
                return true;
            } catch (e) {
                return false;
            }
        },
    };

    // ===========================================
    // ROUTER
    // ===========================================
    
    const Router = {
        currentRoute: null,
        routes: {},
        beforeHooks: [],
        afterHooks: [],
        
        /**
         * Initialize router
         */
        init: function() {
            this.handleRouteChange();
            window.addEventListener('popstate', () => this.handleRouteChange());
            document.addEventListener('click', (e) => {
                const link = e.target.closest('[data-link]');
                if (link) {
                    e.preventDefault();
                    const href = link.getAttribute('href');
                    if (href && !href.startsWith('http')) {
                        this.navigate(href);
                    }
                }
            });
        },
        
        /**
         * Register route
         */
        register: function(path, handler) {
            this.routes[path] = handler;
        },
        
        /**
         * Navigate to path
         */
        navigate: function(path, replace = false) {
            if (replace) {
                window.history.replaceState(null, '', path);
            } else {
                window.history.pushState(null, '', path);
            }
            this.handleRouteChange();
        },
        
        /**
         * Handle route change
         */
        handleRouteChange: async function() {
            const path = window.location.pathname;
            const route = this.matchRoute(path);
            
            // Run before hooks
            for (const hook of this.beforeHooks) {
                const result = await hook(path, route);
                if (result === false) return;
            }
            
            this.currentRoute = path;
            
            // Execute route handler
            if (route && route.handler) {
                try {
                    await route.handler(route.params);
                } catch (error) {
                    console.error('Route handler error:', error);
                    AppUI.showToast('An error occurred while loading the page', 'error');
                }
            } else {
                this.handleNotFound();
            }
            
            // Run after hooks
            for (const hook of this.afterHooks) {
                await hook(path, route);
            }
            
            // Update active links
            this.updateActiveLinks(path);
        },
        
        /**
         * Match route to handler
         */
        matchRoute: function(path) {
            // Exact match
            if (this.routes[path]) {
                return { path, handler: this.routes[path], params: {} };
            }
            
            // Pattern match
            for (const [pattern, handler] of Object.entries(this.routes)) {
                const params = this.matchPattern(pattern, path);
                if (params !== null) {
                    return { path, handler, params };
                }
            }
            
            return null;
        },
        
        /**
         * Match URL pattern
         */
        matchPattern: function(pattern, path) {
            const patternParts = pattern.split('/').filter(Boolean);
            const pathParts = path.split('/').filter(Boolean);
            
            if (patternParts.length !== pathParts.length) {
                return null;
            }
            
            const params = {};
            
            for (let i = 0; i < patternParts.length; i++) {
                if (patternParts[i].startsWith(':')) {
                    params[patternParts[i].slice(1)] = pathParts[i];
                } else if (patternParts[i] !== pathParts[i]) {
                    return null;
                }
            }
            
            return params;
        },
        
        /**
         * Handle 404
         */
        handleNotFound: function() {
            const container = document.getElementById('app');
            if (container) {
                container.innerHTML = `
                    <div class="flex items-center justify-center min-h-screen">
                        <div class="text-center">
                            <h1 class="text-6xl font-bold text-primary mb-4">404</h1>
                            <p class="text-xl text-secondary mb-8">Page not found</p>
                            <a href="/" class="btn btn-primary">Go Home</a>
                        </div>
                    </div>
                `;
            }
        },
        
        /**
         * Update active links
         */
        updateActiveLinks: function(path) {
            document.querySelectorAll('[data-link]').forEach(link => {
                const href = link.getAttribute('href');
                if (href === path || (href !== '/' && path.startsWith(href))) {
                    link.classList.add('active');
                } else {
                    link.classList.remove('active');
                }
            });
        },
        
        /**
         * Add before hook
         */
        before: function(hook) {
            this.beforeHooks.push(hook);
        },
        
        /**
         * Add after hook
         */
        after: function(hook) {
            this.afterHooks.push(hook);
        },
    };

    // ===========================================
    // FORM VALIDATION
    // ===========================================
    
    const Validator = {
        rules: {
            required: {
                validate: function(value) {
                    return value !== null && value !== undefined && value.toString().trim() !== '';
                },
                message: 'This field is required',
            },
            email: {
                validate: function(value) {
                    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    return regex.test(value);
                },
                message: 'Please enter a valid email address',
            },
            minLength: {
                validate: function(value, min) {
                    return value && value.length >= min;
                },
                message: function(min) {
                    return `Minimum ${min} characters required`;
                },
            },
            maxLength: {
                validate: function(value, max) {
                    return !value || value.length <= max;
                },
                message: function(max) {
                    return `Maximum ${max} characters allowed`;
                },
            },
            min: {
                validate: function(value, min) {
                    return parseFloat(value) >= min;
                },
                message: function(min) {
                    return `Minimum value is ${min}`;
                },
            },
            max: {
                validate: function(value, max) {
                    return !value || parseFloat(value) <= max;
                },
                message: function(max) {
                    return `Maximum value is ${max}`;
                },
            },
            numeric: {
                validate: function(value) {
                    return !value || /^\d+$/.test(value);
                },
                message: 'Please enter a valid number',
            },
            alpha: {
                validate: function(value) {
                    return !value || /^[a-zA-Z]+$/.test(value);
                },
                message: 'Only letters are allowed',
            },
            alphanumeric: {
                validate: function(value) {
                    return !value || /^[a-zA-Z0-9]+$/.test(value);
                },
                message: 'Only letters and numbers are allowed',
            },
            url: {
                validate: function(value) {
                    try {
                        new URL(value);
                        return true;
                    } catch {
                        return false;
                    }
                },
                message: 'Please enter a valid URL',
            },
            phone: {
                validate: function(value) {
                    const regex = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/;
                    return !value || regex.test(value);
                },
                message: 'Please enter a valid phone number',
            },
            match: {
                validate: function(value, matchValue) {
                    return value === matchValue;
                },
                message: 'Values do not match',
            },
            password: {
                validate: function(value) {
                    // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
                    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
                    return regex.test(value);
                },
                message: 'Password must be at least 8 characters with uppercase, lowercase, and number',
            },
        },
        
        /**
         * Validate single field
         */
        validateField: function(field, rules) {
            const value = field.value;
            const errors = [];
            
            for (const [rule, ruleValue] of Object.entries(rules)) {
                if (rule === 'custom') continue;
                
                const validator = this.rules[rule];
                if (!validator) continue;
                
                const isValid = typeof validator.validate === 'function' 
                    ? validator.validate(value, ruleValue) 
                    : validator.validate(value);
                
                if (!isValid) {
                    const message = typeof validator.message === 'function' 
                        ? validator.message(ruleValue) 
                        : validator.message;
                    errors.push(message);
                }
            }
            
            return errors;
        },
        
        /**
         * Validate form
         */
        validateForm: function(form, validationRules) {
            const errors = {};
            let isValid = true;
            
            for (const [fieldName, rules] of Object.entries(validationRules)) {
                const field = form.querySelector(`[name="${fieldName}"]`);
                if (!field) continue;
                
                const fieldErrors = this.validateField(field, rules);
                if (fieldErrors.length > 0) {
                    errors[fieldName] = fieldErrors;
                    isValid = false;
                    
                    // Show error on field
                    this.showFieldError(field, fieldErrors[0]);
                } else {
                    this.clearFieldError(field);
                }
            }
            
            return { isValid, errors };
        },
        
        /**
         * Show field error
         */
        showFieldError: function(field, message) {
            const formGroup = field.closest('.form-group') || field.parentElement;
            let errorElement = formGroup.querySelector('.form-error');
            
            if (!errorElement) {
                errorElement = document.createElement('div');
                errorElement.className = 'form-error';
                formGroup.appendChild(errorElement);
            }
            
            errorElement.textContent = message;
            field.classList.add('error');
            field.classList.remove('success');
        },
        
        /**
         * Clear field error
         */
        clearFieldError: function(field) {
            const formGroup = field.closest('.form-group') || field.parentElement;
            const errorElement = formGroup.querySelector('.form-error');
            
            if (errorElement) {
                errorElement.remove();
            }
            
            field.classList.remove('error');
        },
        
        /**
         * Clear all form errors
         */
        clearFormErrors: function(form) {
            form.querySelectorAll('.form-error').forEach(el => el.remove());
            form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
            form.querySelectorAll('.success').forEach(el => el.classList.remove('success'));
        },
    };

    // ===========================================
    // UI COMPONENTS
    // ===========================================
    
    const AppUI = {
        /**
         * Show toast notification
         */
        showToast: function(message, type = 'info', duration = AppConfig.toastDuration) {
            const container = this.getToastContainer();
            
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.innerHTML = `
                <div class="toast-icon">
                    ${this.getToastIcon(type)}
                </div>
                <div class="toast-content">
                    <p class="toast-message">${message}</p>
                </div>
                <button class="toast-close" onclick="this.parentElement.remove()">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </button>
            `;
            
            container.appendChild(toast);
            
            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(100%)';
                setTimeout(() => toast.remove(), 300);
            }, duration);
        },
        
        /**
         * Get toast container
         */
        getToastContainer: function() {
            let container = document.querySelector('.toast-container');
            if (!container) {
                container = document.createElement('div');
                container.className = 'toast-container';
                document.body.appendChild(container);
            }
            return container;
        },
        
        /**
         * Get toast icon
         */
        getToastIcon: function(type) {
            const icons = {
                success: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
                error: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>',
                warning: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
                info: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>',
            };
            return icons[type] || icons.info;
        },
        
        /**
         * Show modal
         */
        showModal: function(options) {
            const {
                title = '',
                content = '',
                size = 'md',
                onConfirm = null,
                onCancel = null,
                confirmText = 'Confirm',
                cancelText = 'Cancel',
                confirmClass = 'btn-primary',
            } = options;
            
            const modal = document.createElement('div');
            modal.className = 'modal-backdrop';
            modal.innerHTML = `
                <div class="modal modal-${size}">
                    <div class="modal-header">
                        <h3 class="modal-title">${title}</h3>
                        <button class="modal-close" data-close-modal>
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                    ${onConfirm ? `
                    <div class="modal-footer">
                        <button class="btn btn-secondary" data-close-modal>${cancelText}</button>
                        <button class="btn ${confirmClass}" data-confirm-modal>${confirmText}</button>
                    </div>
                    ` : ''}
                </div>
            `;
            
            document.body.appendChild(modal);
            document.body.style.overflow = 'hidden';
            
            // Trigger animation
            requestAnimationFrame(() => {
                modal.classList.add('active');
                modal.querySelector('.modal').classList.add('active');
            });
            
            // Event listeners
            modal.querySelectorAll('[data-close-modal]').forEach(btn => {
                btn.addEventListener('click', () => this.closeModal(modal));
            });
            
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    if (onCancel) onCancel();
                    this.closeModal(modal);
                }
            });
            
            if (onConfirm) {
                modal.querySelector('[data-confirm-modal]').addEventListener('click', () => {
                    onConfirm();
                    this.closeModal(modal);
                });
            }
            
            return modal;
        },
        
        /**
         * Close modal
         */
        closeModal: function(modal) {
            modal.classList.remove('active');
            modal.querySelector('.modal').classList.remove('active');
            document.body.style.overflow = '';
            
            setTimeout(() => modal.remove(), 300);
        },
        
        /**
         * Show loading overlay
         */
        showLoading: function(target = document.body) {
            const overlay = document.createElement('div');
            overlay.className = 'loading-overlay';
            overlay.id = 'loading-overlay';
            overlay.innerHTML = '<div class="spinner"></div>';
            target.appendChild(overlay);
            return overlay;
        },
        
        /**
         * Hide loading overlay
         */
        hideLoading: function() {
            const overlay = document.getElementById('loading-overlay');
            if (overlay) overlay.remove();
        },
        
        /**
         * Show confirm dialog
         */
        confirm: function(message, title = 'Confirm') {
            return new Promise((resolve) => {
                this.showModal({
                    title,
                    content: `<p class="text-secondary">${message}</p>`,
                    confirmText: 'Yes',
                    cancelText: 'No',
                    onConfirm: () => resolve(true),
                    onCancel: () => resolve(false),
                });
            });
        },
        
        /**
         * Toggle theme
         */
        toggleTheme: function() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            html.setAttribute('data-theme', newTheme);
            Storage.set(AppConfig.storageKeys.theme, newTheme);
            
            // Update icons
            const sunIcon = document.querySelector('.theme-icon-sun');
            const moonIcon = document.querySelector('.theme-icon-moon');
            
            if (sunIcon && moonIcon) {
                sunIcon.classList.toggle('hidden', newTheme !== 'dark');
                moonIcon.classList.toggle('hidden', newTheme !== 'light');
            }
        },
        
        /**
         * Init theme
         */
        initTheme: function() {
            const savedTheme = Storage.get(AppConfig.storageKeys.theme);
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const theme = savedTheme || (prefersDark ? 'dark' : 'light');
            
            document.documentElement.setAttribute('data-theme', theme);
        },
        
        /**
         * Init sidebar
         */
        initSidebar: function() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('sidebar-overlay');
            const toggleBtn = document.getElementById('mobile-menu-btn');
            
            if (!sidebar) return;
            
            const savedState = Storage.get(AppConfig.storageKeys.sidebar, 'expanded');
            
            const toggle = () => {
                const isExpanded = sidebar.classList.contains('translate-x-0') || 
                                  !sidebar.classList.contains('-translate-x-full');
                
                if (isExpanded) {
                    sidebar.classList.add('-translate-x-full');
                    sidebar.classList.remove('translate-x-0');
                    if (overlay) {
                        overlay.classList.add('hidden');
                    }
                    Storage.set(AppConfig.storageKeys.sidebar, 'collapsed');
                } else {
                    sidebar.classList.remove('-translate-x-full');
                    sidebar.classList.add('translate-x-0');
                    if (overlay) {
                        overlay.classList.remove('hidden');
                    }
                    Storage.set(AppConfig.storageKeys.sidebar, 'expanded');
                }
            };
            
            if (toggleBtn) {
                toggleBtn.addEventListener('click', toggle);
            }
            
            if (overlay) {
                overlay.addEventListener('click', toggle);
            }
        },
        
        /**
         * Init dropdowns
         */
        initDropdowns: function() {
            document.querySelectorAll('.dropdown').forEach(dropdown => {
                const trigger = dropdown.querySelector('[data-dropdown-trigger]');
                const menu = dropdown.querySelector('.dropdown-menu');
                
                if (!trigger || !menu) return;
                
                trigger.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const isActive = dropdown.classList.contains('active');
                    
                    // Close all dropdowns
                    document.querySelectorAll('.dropdown.active').forEach(d => {
                        d.classList.remove('active');
                    });
                    
                    if (!isActive) {
                        dropdown.classList.add('active');
                    }
                });
            });
            
            // Close dropdowns on click outside
            document.addEventListener('click', () => {
                document.querySelectorAll('.dropdown.active').forEach(d => {
                    d.classList.remove('active');
                });
            });
        },
        
        /**
         * Init tooltips
         */
        initTooltips: function() {
            const tooltipElements = document.querySelectorAll('[data-tooltip]');
            
            tooltipElements.forEach(el => {
                const tooltip = document.createElement('div');
                tooltip.className = 'tooltip';
                tooltip.textContent = el.getAttribute('data-tooltip');
                tooltip.setAttribute('role', 'tooltip');
                
                el.addEventListener('mouseenter', () => {
                    const rect = el.getBoundingClientRect();
                    tooltip.style.top = `${rect.top - 40}px`;
                    tooltip.style.left = `${rect.left + (rect.width / 2) - 50}px`;
                    document.body.appendChild(tooltip);
                });
                
                el.addEventListener('mouseleave', () => {
                    tooltip.remove();
                });
            });
        },
        
        /**
         * Init tabs
         */
        initTabs: function() {
            document.querySelectorAll('.tabs').forEach(tabs => {
                const tabButtons = tabs.querySelectorAll('.tab');
                
                tabButtons.forEach(button => {
                    button.addEventListener('click', () => {
                        const target = button.getAttribute('data-tab');
                        
                        // Remove active from all tabs
                        tabButtons.forEach(btn => btn.classList.remove('active'));
                        tabs.querySelectorAll('.tab-content').forEach(content => {
                            content.classList.remove('active');
                        });
                        
                        // Add active to clicked tab
                        button.classList.add('active');
                        const targetContent = tabs.querySelector(`#${target}`);
                        if (targetContent) {
                            targetContent.classList.add('active');
                        }
                    });
                });
            });
        },
        
        /**
         * Init forms
         */
        initForms: function() {
            // Form validation on blur
            document.querySelectorAll('.form-input, .form-textarea, .form-select').forEach(field => {
                field.addEventListener('blur', function() {
                    const formGroup = this.closest('.form-group');
                    if (!formGroup) return;
                    
                    const validationRules = formGroup.dataset.validation;
                    if (!validationRules) return;
                    
                    const rules = JSON.parse(validationRules);
                    const errors = Validator.validateField(this, rules);
                    
                    if (errors.length > 0) {
                        Validator.showFieldError(this, errors[0]);
                    } else if (this.value) {
                        this.classList.remove('error');
                        this.classList.add('success');
                    }
                });
                
                // Clear error on input
                field.addEventListener('input', function() {
                    if (this.classList.contains('error')) {
                        Validator.clearFieldError(this);
                    }
                });
            });
        },
        
        /**
         * Render pagination
         */
        renderPagination: function(options) {
            const {
                currentPage = 1,
                totalPages = 1,
                onPageChange = () => {},
            } = options;
            
            if (totalPages <= 1) return '';
            
            let html = '<div class="pagination">';
            
            // Previous button
            html += `
                <button class="pagination-btn" ${currentPage === 1 ? 'disabled' : ''} 
                        data-page="${currentPage - 1}">
                    &laquo; Prev
                </button>
            `;
            
            // Page numbers
            const maxVisible = 5;
            let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
            let endPage = Math.min(totalPages, startPage + maxVisible - 1);
            
            if (endPage - startPage + 1 < maxVisible) {
                startPage = Math.max(1, endPage - maxVisible + 1);
            }
            
            if (startPage > 1) {
                html += `<button class="pagination-btn" data-page="1">1</button>`;
                if (startPage > 2) {
                    html += `<span class="pagination-ellipsis">...</span>`;
                }
            }
            
            for (let i = startPage; i <= endPage; i++) {
                html += `
                    <button class="pagination-btn ${i === currentPage ? 'active' : ''}" 
                            data-page="${i}">
                        ${i}
                    </button>
                `;
            }
            
            if (endPage < totalPages) {
                if (endPage < totalPages - 1) {
                    html += `<span class="pagination-ellipsis">...</span>`;
                }
                html += `<button class="pagination-btn" data-page="${totalPages}">${totalPages}</button>`;
            }
            
            // Next button
            html += `
                <button class="pagination-btn" ${currentPage === totalPages ? 'disabled' : ''} 
                        data-page="${currentPage + 1}">
                    Next &raquo;
                </button>
            `;
            
            html += '</div>';
            
            return html;
        },
        
        /**
         * Render table
         */
        renderTable: function(options) {
            const {
                columns = [],
                data = [],
                emptyMessage = 'No data available',
                sortable = false,
            } = options;
            
            if (data.length === 0) {
                return `
                    <div class="text-center py-12">
                        <p class="text-muted">${emptyMessage}</p>
                    </div>
                `;
            }
            
            let html = '<div class="table-container"><table class="table">';
            
            // Header
            html += '<thead><tr>';
            columns.forEach(col => {
                html += `<th ${col.sortable ? 'data-sort="' + col.key + '"' : ''}>${col.label}</th>`;
            });
            html += '</tr></thead>';
            
            // Body
            html += '<tbody>';
            data.forEach(row => {
                html += '<tr>';
                columns.forEach(col => {
                    const value = Utils.getNestedValue(row, col.key);
                    html += `<td>${col.render ? col.render(value, row) : value}</td>`;
                });
                html += '</tr>';
            });
            html += '</tbody></table></div>';
            
            return html;
        },
        
        /**
         * Render card
         */
        renderCard: function(options) {
            const {
                title = '',
                subtitle = '',
                content = '',
                footer = '',
                interactive = false,
            } = options;
            
            return `
                <div class="card ${interactive ? 'card-interactive' : ''}">
                    ${title ? `
                        <div class="card-header">
                            <h3 class="card-title">${title}</h3>
                            ${subtitle ? `<p class="card-subtitle">${subtitle}</p>` : ''}
                        </div>
                    ` : ''}
                    <div class="card-body">
                        ${content}
                    </div>
                    ${footer ? `
                        <div class="card-footer">
                            ${footer}
                        </div>
                    ` : ''}
                </div>
            `;
        },
        
        /**
         * Render alert
         */
        renderAlert: function(options) {
            const {
                type = 'info',
                title = '',
                message = '',
                dismissible = false,
            } = options;
            
            return `
                <div class="alert alert-${type} ${dismissible ? 'alert-dismissible' : ''}">
                    <div class="alert-icon">
                        ${this.getToastIcon(type)}
                    </div>
                    <div class="alert-content">
                        ${title ? `<p class="alert-title">${title}</p>` : ''}
                        <p class="alert-message">${message}</p>
                    </div>
                    ${dismissible ? `
                        <button class="alert-close" onclick="this.parentElement.remove()">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    ` : ''}
                </div>
            `;
        },
        
        /**
         * Render skeleton loader
         */
        renderSkeleton: function(type = 'text', count = 1) {
            let html = '';
            for (let i = 0; i < count; i++) {
                html += `<div class="skeleton skeleton-${type}"></div>`;
            }
            return html;
        },
        
        /**
         * Render badge
         */
        renderBadge: function(text, type = 'primary') {
            return `<span class="badge badge-${type}">${text}</span>`;
        },
        
        /**
         * Render avatar
         */
        renderAvatar: function(options) {
            const {
                src = '',
                alt = '',
                initials = '',
                size = 'md',
            } = options;
            
            const sizeClass = size === 'sm' ? 'avatar-sm' : size === 'lg' ? 'avatar-lg' : size === 'xl' ? 'avatar-xl' : '';
            
            if (src) {
                return `<div class="avatar ${sizeClass}"><img src="${src}" alt="${alt}"></div>`;
            }
            
            return `<div class="avatar ${sizeClass}">${initials}</div>`;
        },
    };

    // ===========================================
    // AUTHENTICATION
    // ===========================================
    
    const Auth = {
        currentUser: null,
        
        /**
         * Check if user is authenticated
         */
        isAuthenticated: function() {
            return this.currentUser !== null || Storage.get(AppConfig.storageKeys.user) !== null;
        },
        
        /**
         * Get current user
         */
        getUser: function() {
            return this.currentUser || Storage.get(AppConfig.storageKeys.user);
        },
        
        /**
         * Set current user
         */
        setUser: function(user) {
            this.currentUser = user;
            if (user) {
                Storage.set(AppConfig.storageKeys.user, user);
            } else {
                Storage.remove(AppConfig.storageKeys.user);
            }
        },
        
        /**
         * Login user
         */
        login: async function(username, password) {
            try {
                const response = await fetch(`${AppConfig.authUrl}/login/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken(),
                    },
                    credentials: 'include',
                    body: JSON.stringify({ username, password }),
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Login failed');
                }
                
                // Get user data
                const userResponse = await fetch(`${AppConfig.authUrl}/user/`, {
                    credentials: 'include',
                });
                
                if (userResponse.ok) {
                    const userData = await userResponse.json();
                    this.setUser(userData);
                }
                
                // Dispatch event
                window.dispatchEvent(new CustomEvent('auth:login', { detail: data }));
                
                AppUI.showToast('Login successful!', 'success');
                
                return data;
            } catch (error) {
                AppUI.showToast(error.message, 'error');
                throw error;
            }
        },
        
        /**
         * Register user
         */
        register: async function(userData) {
            try {
                const response = await fetch(`${AppConfig.apiBaseUrl}/accounts/users/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken(),
                    },
                    credentials: 'include',
                    body: JSON.stringify(userData),
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    const error = data.error || Object.values(data).flat()[0] || 'Registration failed';
                    throw new Error(error);
                }
                
                AppUI.showToast('Registration successful! Please check your email to verify your account.', 'success');
                
                return data;
            } catch (error) {
                AppUI.showToast(error.message, 'error');
                throw error;
            }
        },
        
        /**
         * Logout user
         */
        logout: async function() {
            try {
                await fetch(`${AppConfig.authUrl}/logout/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCSRFToken(),
                    },
                    credentials: 'include',
                });
                
                this.setUser(null);
                
                // Dispatch event
                window.dispatchEvent(new CustomEvent('auth:logout', {}));
                
                AppUI.showToast('You have been logged out', 'success');
                
                // Redirect to home
                Router.navigate('/');
            } catch (error) {
                console.error('Logout error:', error);
                // Still clear local state even if server request fails
                this.setUser(null);
                Router.navigate('/');
            }
        },
        
        /**
         * Request password reset
         */
        requestPasswordReset: async function(email) {
            try {
                const response = await fetch(`${AppConfig.authUrl}/password/reset/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email }),
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Password reset request failed');
                }
                
                AppUI.showToast('If an account exists with this email, you will receive password reset instructions.', 'success');
                
                return data;
            } catch (error) {
                AppUI.showToast(error.message, 'error');
                throw error;
            }
        },
        
        /**
         * Reset password
         */
        resetPassword: async function(uid, token, newPassword) {
            try {
                const response = await fetch(`${AppConfig.authUrl}/password/reset/confirm/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        uid,
                        token,
                        new_password: newPassword,
                    }),
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Password reset failed');
                }
                
                AppUI.showToast('Password has been reset successfully!', 'success');
                
                return data;
            } catch (error) {
                AppUI.showToast(error.message, 'error');
                throw error;
            }
        },
        
        /**
         * Get CSRF token
         */
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
        
        /**
         * Check auth status on load
         */
        checkAuthStatus: async function() {
            if (!Storage.get(AppConfig.storageKeys.user)) {
                return;
            }
            
            try {
                const response = await fetch(`${AppConfig.authUrl}/user/`, {
                    credentials: 'include',
                });
                
                if (response.ok) {
                    const userData = await response.json();
                    this.setUser(userData);
                } else {
                    this.setUser(null);
                }
            } catch (error) {
                console.error('Auth check error:', error);
                this.setUser(null);
            }
        },
    };

    // ===========================================
    // DATA FETCHING
    // ===========================================
    
    const DataFetcher = {
        /**
         * Fetch with loading state
         */
        fetch: async function(url, options = {}) {
            const loadingEl = options.loadingEl || document.getElementById('app');
            
            // Show loading
            if (options.showLoading !== false && loadingEl) {
                AppUI.showLoading(loadingEl);
            }
            
            try {
                const response = await fetch(url, {
                    ...options,
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'X-CSRFToken': Auth.getCSRFToken(),
                        ...options.headers,
                    },
                    credentials: 'include',
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Request failed');
                }
                
                return data;
            } catch (error) {
                AppUI.showToast(error.message, 'error');
                throw error;
            } finally {
                if (options.showLoading !== false) {
                    AppUI.hideLoading();
                }
            }
        },
        
        /**
         * Fetch paginated data
         */
        fetchPaginated: async function(url, page = 1, pageSize = AppConfig.defaultPageSize) {
            const params = new URLSearchParams({
                page: page.toString(),
                page_size: pageSize.toString(),
            });
            
            return this.fetch(`${url}?${params}`);
        },
        
        /**
         * Fetch and render list
         */
        fetchAndRender: async function(url, options = {}) {
            const {
                containerId = 'app',
                renderFunc = (data) => data.results || data,
                emptyMessage = 'No data found',
                loadingMessage = 'Loading...',
            } = options;
            
            const container = document.getElementById(containerId);
            if (!container) return;
            
            container.innerHTML = `<div class="text-center py-12">${loadingMessage}</div>`;
            
            try {
                const data = await this.fetch(url);
                const items = renderFunc(data);
                
                if (!items || items.length === 0) {
                    container.innerHTML = `<div class="text-center py-12 text-muted">${emptyMessage}</div>`;
                    return null;
                }
                
                return data;
            } catch (error) {
                container.innerHTML = `
                    <div class="alert alert-error">
                        <p>${error.message}</p>
                        <button class="btn btn-sm btn-outline" onclick="DataFetcher.fetchAndRender('${url}', ${JSON.stringify(options).replace(/"/g, '"')})">
                            Retry
                        </button>
                    </div>
                `;
                throw error;
            }
        },
    };

    // ===========================================
    // INITIALIZATION
    // ===========================================
    
    const App = {
        /**
         * Initialize application
         */
        init: function() {
            console.log(`${AppConfig.appName} v${AppConfig.appVersion} initializing...`);
            
            // Initialize components
            AppUI.initTheme();
            AppUI.initSidebar();
            AppUI.initDropdowns();
            AppUI.initTooltips();
            AppUI.initTabs();
            AppUI.initForms();
            
            // Initialize router
            Router.init();
            
            // Check authentication
            Auth.checkAuthStatus();
            
            // Register auth event listeners
            this.registerEventListeners();
            
            // Initialize Lucide icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
            
            console.log('Application initialized successfully');
        },
        
        /**
         * Register event listeners
         */
        registerEventListeners: function() {
            // Auth events
            window.addEventListener('auth:unauthorized', () => {
                Auth.setUser(null);
                AppUI.showToast('Your session has expired. Please log in again.', 'warning');
                Router.navigate('/login/');
            });
            
            window.addEventListener('auth:login', () => {
                Router.navigate('/dashboard/');
            });
            
            // Logout button
            document.addEventListener('click', (e) => {
                const logoutBtn = e.target.closest('[data-logout]');
                if (logoutBtn) {
                    e.preventDefault();
                    Auth.logout();
                }
            });
            
            // Theme toggle
            document.addEventListener('click', (e) => {
                const themeBtn = e.target.closest('#theme-toggle');
                if (themeBtn) {
                    AppUI.toggleTheme();
                }
            });
            
            // Mobile menu toggle
            document.addEventListener('click', (e) => {
                const menuBtn = e.target.closest('#mobile-menu-btn');
                if (menuBtn) {
                    const sidebar = document.getElementById('sidebar');
                    const overlay = document.getElementById('sidebar-overlay');
                    if (sidebar) {
                        sidebar.classList.toggle('-translate-x-full');
                        sidebar.classList.toggle('translate-x-0');
                    }
                    if (overlay) {
                        overlay.classList.toggle('hidden');
                    }
                }
            });
            
            // Close dropdowns on escape
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    document.querySelectorAll('.dropdown.active').forEach(d => {
                        d.classList.remove('active');
                    });
                }
            });
            
            // Handle pagination clicks
            document.addEventListener('click', (e) => {
                const pageBtn = e.target.closest('[data-page]');
                if (pageBtn && window.dispatchEvent) {
                    const event = new CustomEvent('pagination:change', {
                        detail: { page: parseInt(pageBtn.dataset.page) }
                    });
                    window.dispatchEvent(event);
                }
            });
        },
    };

    // ===========================================
    // EXPOSE TO GLOBAL SCOPE
    // ===========================================
    
    window.App = {
        config: AppConfig,
        utils: Utils,
        storage: Storage,
        router: Router,
        validator: Validator,
        ui: AppUI,
        auth: Auth,
        data: DataFetcher,
        init: () => App.init(),
    };
    
    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => App.init());
    } else {
        App.init();
    }

})();
