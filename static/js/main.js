/**
 * 60 SECONDS TO NAPOLI - Core JavaScript Library
 * Shared utilities and components for consistent functionality
 */

// ===== NAMESPACE =====
const Napoli = window.Napoli || {};

// ===== CONFIGURATION =====
Napoli.config = {
    apiBaseUrl: '/api',
    toastDuration: 4000,
    animationDuration: 300,
    debounceDelay: 300
};

// ===== UTILITY FUNCTIONS =====
Napoli.utils = {
    /**
     * Debounce function to limit execution rate
     */
    debounce(func, wait = Napoli.config.debounceDelay) {
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
     * Throttle function to limit execution frequency
     */
    throttle(func, limit) {
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
     * Format currency
     */
    formatCurrency(amount, currency = '€') {
        return `${parseFloat(amount).toFixed(2)} ${currency}`;
    },

    /**
     * Format date
     */
    formatDate(date, locale = 'fr-FR') {
        return new Date(date).toLocaleDateString(locale, {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    /**
     * Generate unique ID
     */
    generateId() {
        return 'id_' + Math.random().toString(36).substr(2, 9);
    },

    /**
     * Get CSRF token from cookies
     */
    getCsrfToken() {
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
     * Safe JSON parse
     */
    safeJsonParse(str, fallback = null) {
        try {
            return JSON.parse(str);
        } catch (e) {
            return fallback;
        }
    },

    /**
     * Check if element is in viewport
     */
    isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
};

// ===== API SERVICE =====
Napoli.api = {
    /**
     * Make API request
     */
    async request(endpoint, options = {}) {
        const url = endpoint.startsWith('http') ? endpoint : `${Napoli.config.apiBaseUrl}${endpoint}`;
        
        const defaultHeaders = {
            'Content-Type': 'application/json',
            'X-CSRFToken': Napoli.utils.getCsrfToken()
        };

        const config = {
            ...options,
            headers: {
                ...defaultHeaders,
                ...options.headers
            }
        };

        if (config.body && typeof config.body === 'object') {
            config.body = JSON.stringify(config.body);
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || data.error || 'An error occurred');
            }
            
            return { success: true, data };
        } catch (error) {
            console.error('API Error:', error);
            return { success: false, error: error.message };
        }
    },

    get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },

    post(endpoint, data) {
        return this.request(endpoint, { method: 'POST', body: data });
    },

    put(endpoint, data) {
        return this.request(endpoint, { method: 'PUT', body: data });
    },

    delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
};

// ===== TOAST NOTIFICATIONS =====
Napoli.toast = {
    container: null,

    init() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            this.container.setAttribute('aria-live', 'polite');
            document.body.appendChild(this.container);
        }
    },

    show(message, type = 'info', duration = Napoli.config.toastDuration) {
        this.init();

        const toast = document.createElement('div');
        toast.className = `toast toast-${type} show fade-in`;
        toast.setAttribute('role', 'alert');
        
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };

        toast.innerHTML = `
            <div class="toast-header">
                <i class="fas ${icons[type] || icons.info} me-2"></i>
                <strong class="me-auto">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
                <button type="button" class="btn-close btn-close-white" aria-label="Close"></button>
            </div>
            <div class="toast-body">${message}</div>
        `;

        this.container.appendChild(toast);

        // Close button handler
        toast.querySelector('.btn-close').addEventListener('click', () => {
            this.hide(toast);
        });

        // Auto hide
        if (duration > 0) {
            setTimeout(() => this.hide(toast), duration);
        }

        return toast;
    },

    hide(toast) {
        toast.classList.remove('show');
        toast.classList.add('hide');
        setTimeout(() => toast.remove(), 300);
    },

    success(message) { return this.show(message, 'success'); },
    error(message) { return this.show(message, 'error'); },
    warning(message) { return this.show(message, 'warning'); },
    info(message) { return this.show(message, 'info'); }
};

// ===== CART MANAGEMENT =====
Napoli.cart = {
    items: [],
    listeners: [],

    init() {
        const saved = localStorage.getItem('napoli_cart');
        this.items = Napoli.utils.safeJsonParse(saved, []);
        this.updateUI();
    },

    add(item) {
        const existing = this.items.find(i => i.id === item.id);
        if (existing) {
            existing.quantity += item.quantity || 1;
        } else {
            this.items.push({ ...item, quantity: item.quantity || 1 });
        }
        this.save();
        Napoli.toast.success(`${item.name} added to cart!`);
    },

    remove(itemId) {
        this.items = this.items.filter(i => i.id !== itemId);
        this.save();
    },

    updateQuantity(itemId, quantity) {
        const item = this.items.find(i => i.id === itemId);
        if (item) {
            if (quantity <= 0) {
                this.remove(itemId);
            } else {
                item.quantity = quantity;
                this.save();
            }
        }
    },

    clear() {
        this.items = [];
        this.save();
    },

    getTotal() {
        return this.items.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0);
    },

    getItemCount() {
        return this.items.reduce((sum, item) => sum + item.quantity, 0);
    },

    save() {
        localStorage.setItem('napoli_cart', JSON.stringify(this.items));
        this.updateUI();
        this.notifyListeners();
    },

    updateUI() {
        const badges = document.querySelectorAll('.cart-badge, .navbar .badge');
        const count = this.getItemCount();
        badges.forEach(badge => {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline-block' : 'none';
        });
    },

    onChange(callback) {
        this.listeners.push(callback);
    },

    notifyListeners() {
        this.listeners.forEach(cb => cb(this.items));
    }
};

// ===== LOADING STATES =====
Napoli.loading = {
    show(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (element) {
            element.classList.add('loading');
            element.setAttribute('data-original-content', element.innerHTML);
            element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            element.disabled = true;
        }
    },

    hide(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (element) {
            element.classList.remove('loading');
            const original = element.getAttribute('data-original-content');
            if (original) {
                element.innerHTML = original;
            }
            element.disabled = false;
        }
    }
};

// ===== SCROLL EFFECTS =====
Napoli.scroll = {
    init() {
        this.handleNavbarScroll();
        this.handleBackToTop();
        this.handleSmoothScroll();
    },

    handleNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        if (!navbar) return;

        const onScroll = Napoli.utils.throttle(() => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }, 100);

        window.addEventListener('scroll', onScroll);
    },

    handleBackToTop() {
        const btn = document.querySelector('.back-to-top');
        if (!btn) return;

        const onScroll = Napoli.utils.throttle(() => {
            if (window.scrollY > 300) {
                btn.classList.add('visible');
            } else {
                btn.classList.remove('visible');
            }
        }, 100);

        window.addEventListener('scroll', onScroll);

        btn.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    },

    handleSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;
                
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    }
};

// ===== FORM VALIDATION =====
Napoli.forms = {
    validate(form) {
        let isValid = true;
        const inputs = form.querySelectorAll('[required]');
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                this.showError(input, 'This field is required');
            } else if (input.type === 'email' && !this.isValidEmail(input.value)) {
                isValid = false;
                this.showError(input, 'Please enter a valid email');
            } else {
                this.clearError(input);
            }
        });

        return isValid;
    },

    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    },

    showError(input, message) {
        input.classList.add('is-invalid');
        let feedback = input.nextElementSibling;
        if (!feedback || !feedback.classList.contains('invalid-feedback')) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            input.parentNode.appendChild(feedback);
        }
        feedback.textContent = message;
    },

    clearError(input) {
        input.classList.remove('is-invalid');
        const feedback = input.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.remove();
        }
    }
};

// ===== MODALS =====
Napoli.modal = {
    show(content, options = {}) {
        const id = options.id || Napoli.utils.generateId();
        const title = options.title || '';
        const size = options.size || '';
        
        const modalHtml = `
            <div class="modal fade" id="${id}" tabindex="-1">
                <div class="modal-dialog ${size ? 'modal-' + size : ''}">
                    <div class="modal-content">
                        ${title ? `
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        ` : ''}
                        <div class="modal-body">${content}</div>
                        ${options.footer ? `<div class="modal-footer">${options.footer}</div>` : ''}
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modalEl = document.getElementById(id);
        const modal = new bootstrap.Modal(modalEl);
        
        modalEl.addEventListener('hidden.bs.modal', () => {
            modalEl.remove();
        });

        modal.show();
        return modal;
    },

    confirm(message, options = {}) {
        return new Promise((resolve) => {
            const id = Napoli.utils.generateId();
            const footer = `
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-primary" id="${id}-confirm">
                    ${options.confirmText || 'Confirm'}
                </button>
            `;

            const modal = this.show(message, {
                title: options.title || 'Confirm',
                footer
            });

            document.getElementById(`${id}-confirm`).addEventListener('click', () => {
                modal.hide();
                resolve(true);
            });

            document.querySelector(`#${id}`).addEventListener('hidden.bs.modal', () => {
                resolve(false);
            });
        });
    }
};

// ===== INITIALIZE =====
document.addEventListener('DOMContentLoaded', () => {
    Napoli.cart.init();
    Napoli.scroll.init();
    
    // Add fade-in animation to main content
    const main = document.querySelector('main');
    if (main) {
        main.classList.add('fade-in');
    }
});

// Export to global
window.Napoli = Napoli;
