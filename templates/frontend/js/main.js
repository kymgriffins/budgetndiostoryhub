/**
 * Budget Ndio Story - Main JavaScript
 * Handles API integration, authentication, and interactivity
 */

(function() {
    'use strict';

    // ============================================
    // Configuration
    // ============================================
    const CONFIG = {
        API_BASE_URL: window.location.origin + '/api',
        CSRF_COOKIE_NAME: 'csrftoken',
        ANIMATION_DURATION: 800,
        DEBOUNCE_DELAY: 250
    };

    // ============================================
    // DOM Elements
    // ============================================
    const elements = {
        preloader: document.getElementById('preloader'),
        header: document.getElementById('header'),
        mobileNav: document.getElementById('mobile-nav'),
        mobileMenuToggle: document.querySelector('.mobile-menu-toggle'),
        chatToggle: document.getElementById('chat-toggle'),
        chatWidget: document.getElementById('chat-widget'),
        chatForm: document.getElementById('chat-form'),
        chatMessages: document.getElementById('chat-messages'),
        authModal: document.getElementById('auth-modal'),
        authTabs: document.querySelectorAll('.auth-tab'),
        loginForm: document.getElementById('login-form'),
        registerForm: document.getElementById('register-form'),
        modalClose: document.querySelector('.modal-close'),
        modalOverlay: document.querySelector('.modal-overlay')
    };

    // ============================================
    // Utility Functions
    // ============================================

    /**
     * Get CSRF token from cookie
     */
    function getCSRFToken() {
        const name = CONFIG.CSRF_COOKIE_NAME + '=';
        const decodedCookie = decodeURIComponent(document.cookie);
        const ca = decodedCookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length);
            }
        }
        return '';
    }

    /**
     * Debounce function
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Show/hide element
     */
    function toggleElement(element, show) {
        if (!element) return;
        if (show) {
            element.classList.remove('hidden');
        } else {
            element.classList.add('hidden');
        }
    }

    /**
     * Show error message
     */
    function showError(elementId, message) {
        const errorElement = document.getElementById(elementId);
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = message ? 'block' : 'none';
        }
    }

    /**
     * Sanitize HTML to prevent XSS
     */
    function sanitizeHTML(str) {
        const temp = document.createElement('div');
        temp.textContent = str;
        return temp.innerHTML;
    }

    // ============================================
    // Preloader
    // ============================================
    function initPreloader() {
        if (elements.preloader) {
            // Hide preloader after page load
            window.addEventListener('load', function() {
                setTimeout(function() {
                    elements.preloader.classList.add('hidden');
                }, 800);
            });
        }
    }

    // ============================================
    // Header Scroll Effect
    // ============================================
    function initHeaderScroll() {
        const header = elements.header;
        if (!header) return;

        let lastScroll = 0;

        window.addEventListener('scroll', debounce(function() {
            const currentScroll = window.pageYOffset;

            if (currentScroll > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }

            lastScroll = currentScroll;
        }, CONFIG.DEBOUNCE_DELAY));
    }

    // ============================================
    // Mobile Navigation
    // ============================================
    function initMobileNav() {
        const toggle = elements.mobileMenuToggle;
        const nav = elements.mobileNav;

        if (!toggle || !nav) return;

        toggle.addEventListener('click', function() {
            const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
            
            toggle.setAttribute('aria-expanded', !isExpanded);
            nav.classList.toggle('open');
            document.body.style.overflow = isExpanded ? '' : 'hidden';
        });

        // Close on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && nav.classList.contains('open')) {
                toggle.setAttribute('aria-expanded', 'false');
                nav.classList.remove('open');
                document.body.style.overflow = '';
            }
        });

        // Close on link click
        nav.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                toggle.setAttribute('aria-expanded', 'false');
                nav.classList.remove('open');
                document.body.style.overflow = '';
            });
        });
    }

    // ============================================
    // Chat Widget
    // ============================================
    function initChatWidget() {
        const toggle = elements.chatToggle;
        const widget = elements.chatWidget;

        if (!toggle || !widget) return;

        toggle.addEventListener('click', function() {
            const isOpen = widget.classList.contains('open');
            widget.classList.toggle('open');
            toggle.setAttribute('aria-expanded', !isOpen);
        });

        // Close on escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && widget.classList.contains('open')) {
                widget.classList.remove('open');
                toggle.setAttribute('aria-expanded', 'false');
            }
        });

        // Handle chat form submission
        if (elements.chatForm) {
            elements.chatForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const input = this.querySelector('input');
                const message = input.value.trim();

                if (message) {
                    addUserMessage(message);
                    input.value = '';
                    
                    // Simulate bot response
                    setTimeout(function() {
                        addBotMessage('Thank you for your message! Our team will get back to you shortly.');
                    }, 1000);
                }
            });
        }
    }

    /**
     * Add user message to chat
     */
    function addUserMessage(message) {
        const messagesContainer = elements.chatMessages;
        if (!messagesContainer) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message user';
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${sanitizeHTML(message)}</p>
            </div>
        `;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    /**
     * Add bot message to chat
     */
    function addBotMessage(message) {
        const messagesContainer = elements.chatMessages;
        if (!messagesContainer) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message bot';
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${sanitizeHTML(message)}</p>
            </div>
        `;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // ============================================
    // Authentication Modal
    // ============================================
    function initAuthModal() {
        // Open modal buttons
        document.querySelectorAll('[data-auth="open"]').forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                openAuthModal();
            });
        });

        // Close modal
        if (elements.modalClose) {
            elements.modalClose.addEventListener('click', closeAuthModal);
        }

        if (elements.modalOverlay) {
            elements.modalOverlay.addEventListener('click', closeAuthModal);
        }

        // Tab switching
        elements.authTabs.forEach(function(tab) {
            tab.addEventListener('click', function() {
                const tabName = this.dataset.tab;
                switchAuthTab(tabName);
            });
        });

        // Close on escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && elements.authModal && elements.authModal.classList.contains('open')) {
                closeAuthModal();
            }
        });
    }

    /**
     * Open auth modal
     */
    function openAuthModal() {
        if (!elements.authModal) return;
        elements.authModal.classList.add('open');
        document.body.style.overflow = 'hidden';
        
        // Focus first input
        setTimeout(function() {
            const firstInput = elements.authModal.querySelector('input');
            if (firstInput) firstInput.focus();
        }, 100);
    }

    /**
     * Close auth modal
     */
    function closeAuthModal() {
        if (!elements.authModal) return;
        elements.authModal.classList.remove('open');
        document.body.style.overflow = '';
        
        // Reset forms
        if (elements.loginForm) elements.loginForm.reset();
        if (elements.registerForm) elements.registerForm.reset();
        showError('login-error', '');
        showError('register-error', '');
    }

    /**
     * Switch auth tab
     */
    function switchAuthTab(tabName) {
        elements.authTabs.forEach(function(tab) {
            tab.classList.toggle('active', tab.dataset.tab === tabName);
        });

        if (tabName === 'login') {
            toggleElement(elements.loginForm, true);
            toggleElement(elements.registerForm, false);
        } else {
            toggleElement(elements.loginForm, false);
            toggleElement(elements.registerForm, true);
        }
    }

    // ============================================
    // API Client
    // ============================================

    /**
     * API Client class for making requests
     */
    class APIClient {
        constructor(baseURL) {
            this.baseURL = baseURL;
        }

        async request(endpoint, options = {}) {
            const url = this.baseURL + endpoint;
            const defaultOptions = {
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                }
            };

            const mergedOptions = {
                ...defaultOptions,
                ...options,
                headers: {
                    ...defaultOptions.headers,
                    ...options.headers
                }
            };

            try {
                const response = await fetch(url, mergedOptions);
                
                // Handle CSRF refresh
                if (response.status === 403) {
                    await this.refreshCSRF();
                    mergedOptions.headers['X-CSRFToken'] = getCSRFToken();
                    const retryResponse = await fetch(url, mergedOptions);
                    if (!retryResponse.ok) {
                        throw new Error(`HTTP error! status: ${retryResponse.status}`);
                    }
                    return await retryResponse.json();
                }

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error('API Error:', error);
                throw error;
            }
        }

        async refreshCSRF() {
            try {
                await fetch(this.baseURL + '/csrf/', {
                    credentials: 'include'
                });
            } catch (error) {
                console.error('CSRF refresh error:', error);
            }
        }

        // Auth endpoints
        async login(email, password) {
            return this.request('/auth/login/', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });
        }

        async register(name, email, password) {
            return this.request('/auth/register/', {
                method: 'POST',
                body: JSON.stringify({ name, email, password })
            });
        }

        async logout() {
            return this.request('/auth/logout/', {
                method: 'POST'
            });
        }

        async getCurrentUser() {
            return this.request('/auth/user/');
        }

        // Content endpoints
        async getReports(params = {}) {
            const queryString = new URLSearchParams(params).toString();
            return this.request('/v1/reports/' + (queryString ? '?' + queryString : ''));
        }

        async getReport(id) {
            return this.request('/v1/reports/' + id + '/');
        }

        async getBlogs(params = {}) {
            const queryString = new URLSearchParams(params).toString();
            return this.request('/v1/blogs/' + (queryString ? '?' + queryString : ''));
        }

        async getStats() {
            return this.request('/v1/stats/');
        }

        async subscribe(email) {
            return this.request('/v1/subscribe/', {
                method: 'POST',
                body: JSON.stringify({ email })
            });
        }
    }

    // Initialize API client
    const api = new APIClient(CONFIG.API_BASE_URL);

    // ============================================
    // Form Handlers
    // ============================================

    /**
     * Handle login form submission
     */
    function initLoginForm() {
        if (!elements.loginForm) return;

        elements.loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const email = this.querySelector('#login-email').value;
            const password = this.querySelector('#login-password').value;

            showError('login-error', '');

            try {
                const response = await api.login(email, password);
                console.log('Login successful:', response);
                
                closeAuthModal();
                
                // Show success message or redirect
                showNotification('Login successful! Welcome back.');
                
                // Update UI to show logged in state
                updateAuthUI(true, response.user);
            } catch (error) {
                console.error('Login error:', error);
                showError('login-error', 'Invalid email or password. Please try again.');
            }
        });
    }

    /**
     * Handle register form submission
     */
    function initRegisterForm() {
        if (!elements.registerForm) return;

        elements.registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const name = this.querySelector('#register-name').value;
            const email = this.querySelector('#register-email').value;
            const password = this.querySelector('#register-password').value;

            showError('register-error', '');

            // Basic validation
            if (password.length < 8) {
                showError('register-error', 'Password must be at least 8 characters.');
                return;
            }

            try {
                const response = await api.register(name, email, password);
                console.log('Registration successful:', response);
                
                closeAuthModal();
                
                // Show success message
                showNotification('Account created successfully! Please check your email to verify.');
                
                // Update UI to show logged in state
                updateAuthUI(true, response.user);
            } catch (error) {
                console.error('Registration error:', error);
                showError('register-error', 'Registration failed. Please try again.');
            }
        });
    }

    /**
     * Update auth UI based on login state
     */
    function updateAuthUI(isLoggedIn, user) {
        const authButtons = document.querySelectorAll('[data-auth]');
        
        authButtons.forEach(function(btn) {
            if (isLoggedIn) {
                if (btn.dataset.auth === 'login') {
                    btn.textContent = user ? user.name : 'My Account';
                    btn.href = '/dashboard/';
                }
            }
        });
    }

    /**
     * Show notification
     */
    function showNotification(message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        
        // Add styles inline for simplicity
        Object.assign(notification.style, {
            position: 'fixed',
            top: '100px',
            right: '20px',
            padding: '16px 24px',
            background: '#10b981',
            color: 'white',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            zIndex: '9999',
            animation: 'slideIn 0.3s ease'
        });
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(function() {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(function() {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // ============================================
    // Stats Animation
    // ============================================

    /**
     * Animate counter from 0 to target value
     */
    function animateCounter(element, target, duration = 2000) {
        if (!element) return;
        
        const start = 0;
        const startTime = performance.now();
        
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Ease out cubic
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            
            const current = Math.floor(start + (target - start) * easeProgress);
            element.textContent = current.toLocaleString() + (target >= 10000 ? '+' : '');
            
            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        
        requestAnimationFrame(update);
    }

    /**
     * Initialize stats animation on scroll
     */
    function initStatsAnimation() {
        const statValues = document.querySelectorAll('.stat-value[data-count]');
        if (!statValues.length) return;

        let animated = false;

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting && !animated) {
                    animated = true;
                    statValues.forEach(function(el) {
                        const target = parseInt(el.dataset.count, 10);
                        animateCounter(el, target);
                    });
                }
            });
        }, { threshold: 0.5 });

        const section = document.querySelector('.stats-section');
        if (section) {
            observer.observe(section);
        }
    }

    // ============================================
    // API Data Loading
    // ============================================

    /**
     * Load reports from API
     */
    async function loadReports() {
        const reportsList = document.getElementById('reports-list');
        if (!reportsList) return;

        try {
            const response = await api.getReports({ limit: 5 });
            
            if (response.results && response.results.length > 0) {
                // Clear existing content
                reportsList.innerHTML = '';
                
                // Render reports
                response.results.forEach(function(report) {
                    const article = document.createElement('article');
                    article.className = 'report-card';
                    article.innerHTML = `
                        <div class="report-meta">
                            <span class="report-type">${sanitizeHTML(report.category || 'National')}</span>
                            <span class="report-date">${report.published_date ? new Date(report.published_date).toLocaleDateString('en-US', { month: 'short', year: 'numeric' }) : ''}</span>
                        </div>
                        <div class="report-content">
                            <h3 class="report-title">${sanitizeHTML(report.title)}</h3>
                            <p class="report-description">${sanitizeHTML(report.summary || '')}</p>
                        </div>
                        <a href="/reports/${report.id}/" class="report-link">
                            Read brief
                            <span class="link-arrow">→</span>
                        </a>
                    `;
                    reportsList.appendChild(article);
                });
            }
        } catch (error) {
            console.error('Error loading reports:', error);
            // Keep static content as fallback
        }
    }

    /**
     * Load stats from API
     */
    async function loadStats() {
        const statsCards = document.querySelectorAll('.stat-card');
        if (!statsCards.length) return;

        try {
            const response = await api.getStats();
            
            if (response) {
                // Update stats if API returns data
                if (response.reports_count !== undefined) {
                    const reportsEl = document.querySelector('.stat-value[data-count]');
                    if (reportsEl) {
                        reportsEl.dataset.count = response.reports_count;
                        animateCounter(reportsEl, response.reports_count);
                    }
                }
            }
        } catch (error) {
            console.error('Error loading stats:', error);
            // Keep static content as fallback
        }
    }

    // ============================================
    // Newsletter Subscription
    // ============================================

    /**
     * Initialize newsletter forms
     */
    function initNewsletterForms() {
        document.querySelectorAll('.newsletter-form').forEach(function(form) {
            form.addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const email = this.querySelector('input[type="email"]').value;
                const button = this.querySelector('button');
                
                button.disabled = true;
                button.textContent = 'Subscribing...';
                
                try {
                    await api.subscribe(email);
                    showNotification('Thank you for subscribing!');
                    form.reset();
                } catch (error) {
                    showNotification('Subscription failed. Please try again.');
                } finally {
                    button.disabled = false;
                    button.textContent = 'Subscribe';
                }
            });
        });
    }

    // ============================================
    // Smooth Scroll for Anchor Links
    // ============================================

    /**
     * Initialize smooth scroll
     */
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
            anchor.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // ============================================
    // Initialize Everything
    // ============================================

    /**
     * Initialize all modules
     */
    function init() {
        initPreloader();
        initHeaderScroll();
        initMobileNav();
        initChatWidget();
        initAuthModal();
        initLoginForm();
        initRegisterForm();
        initStatsAnimation();
        initNewsletterForms();
        initSmoothScroll();
        
        // Load dynamic data
        loadReports();
        loadStats();
        
        // Check auth state
        checkAuthState();
    }

    /**
     * Check authentication state on page load
     */
    async function checkAuthState() {
        try {
            const user = await api.getCurrentUser();
            if (user && user.id) {
                updateAuthUI(true, user);
            }
        } catch (error) {
            // User not authenticated - that's fine
            console.log('User not authenticated');
        }
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose API for external use
    window.BudgetNdioStory = {
        api: api,
        openAuthModal: openAuthModal,
        closeAuthModal: closeAuthModal,
        showNotification: showNotification
    };

})();
