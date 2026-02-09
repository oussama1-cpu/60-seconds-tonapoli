// RTL (Right-to-Left) JavaScript Support

class RTLSupport {
    constructor() {
        this.currentLang = this.detectLanguage();
        this.init();
    }

    init() {
        this.setupLanguageSwitcher();
        this.adjustLayoutForRTL();
        this.setupRTLAnimations();
        this.fixRTLComponents();
    }

    detectLanguage() {
        // Detect language from URL or localStorage
        const path = window.location.pathname;
        if (path.includes('/ar/')) {
            return 'ar';
        } else if (path.includes('/en/')) {
            return 'en';
        }
        return localStorage.getItem('preferredLanguage') || 'en';
    }

    setupLanguageSwitcher() {
        // Add language switcher functionality
        document.addEventListener('click', (e) => {
            if (e.target.matches('.language-switcher a')) {
                e.preventDefault();
                const lang = e.target.dataset.lang || (e.target.textContent.includes('English') ? 'en' : 'ar');
                this.switchLanguage(lang);
            }
        });
    }

    switchLanguage(lang) {
        // Save preference
        localStorage.setItem('preferredLanguage', lang);
        
        // Get current path
        const currentPath = window.location.pathname;
        
        // Switch language in URL
        let newPath;
        if (lang === 'ar') {
            newPath = currentPath.replace('/en/', '/ar/');
            if (!newPath.includes('/ar/')) {
                newPath = '/ar' + currentPath;
            }
        } else {
            newPath = currentPath.replace('/ar/', '/en/');
            if (!newPath.includes('/en/')) {
                newPath = newPath.replace('/ar', '/en');
            }
        }
        
        // Redirect to new language
        window.location.href = newPath;
    }

    adjustLayoutForRTL() {
        if (this.currentLang === 'ar') {
            document.documentElement.setAttribute('dir', 'rtl');
            document.documentElement.setAttribute('lang', 'ar');
            document.body.classList.add('rtl-layout');
            
            // Adjust Bootstrap components for RTL
            this.adjustBootstrapRTL();
            
            // Fix cart sidebar position for RTL
            this.adjustCartSidebarRTL();
            
            // Fix dropdown menus
            this.adjustDropdownsRTL();
            
            // Fix navigation
            this.adjustNavigationRTL();
        }
    }

    adjustBootstrapRTL() {
        // Fix Bootstrap classes for RTL
        const bootstrapFixes = [
            { from: 'ms-auto', to: 'me-auto' },
            { from: 'me-auto', to: 'ms-auto' },
            { from: 'ms-', to: 'me-' },
            { from: 'me-', to: 'ms-' },
            { from: 'text-start', to: 'text-end' },
            { from: 'text-end', to: 'text-start' },
            { from: 'float-start', to: 'float-end' },
            { from: 'float-end', to: 'float-start' }
        ];

        bootstrapFixes.forEach(fix => {
            const elements = document.querySelectorAll(`.${fix.from}`);
            elements.forEach(el => {
                el.classList.remove(fix.from);
                el.classList.add(fix.to);
            });
        });
    }

    adjustCartSidebarRTL() {
        const cartSidebar = document.getElementById('cart-sidebar');
        if (cartSidebar) {
            // Move cart sidebar to left side for RTL
            cartSidebar.style.right = 'auto';
            cartSidebar.style.left = '-400px';
            
            // Adjust open state
            if (cartSidebar.classList.contains('open')) {
                cartSidebar.style.left = '0';
            }
        }
    }

    adjustDropdownsRTL() {
        // Fix dropdown menus to open on the left for RTL
        const dropdowns = document.querySelectorAll('.dropdown-menu');
        dropdowns.forEach(dropdown => {
            dropdown.style.right = 'auto';
            dropdown.style.left = '0';
        });
    }

    adjustNavigationRTL() {
        // Fix navigation for RTL
        const navbarNav = document.querySelector('.navbar-nav');
        if (navbarNav) {
            navbarNav.style.direction = 'rtl';
        }
    }

    setupRTLAnimations() {
        if (this.currentLang === 'ar') {
            // Adjust animations for RTL
            const style = document.createElement('style');
            style.textContent = `
                @keyframes slideInRTL {
                    from { 
                        transform: translateX(20px); 
                        opacity: 0; 
                    }
                    to { 
                        transform: translateX(0); 
                        opacity: 1; 
                    }
                }
                
                .slide-in {
                    animation: slideInRTL 0.3s ease-out;
                }
                
                @keyframes fadeInRTL {
                    from { 
                        opacity: 0; 
                        transform: translateX(20px); 
                    }
                    to { 
                        opacity: 1; 
                        transform: translateX(0); 
                    }
                }
                
                .fade-in {
                    animation: fadeInRTL 0.5s ease-in;
                }
                
                /* Cart animation RTL */
                @keyframes badgeUpdateRTL {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.3); }
                    100% { transform: scale(1); }
                }
                
                .cart-badge-update {
                    animation: badgeUpdateRTL 0.3s ease;
                }
            `;
            document.head.appendChild(style);
        }
    }

    fixRTLComponents() {
        if (this.currentLang === 'ar') {
            // Fix form inputs for RTL
            const formInputs = document.querySelectorAll('input, textarea');
            formInputs.forEach(input => {
                input.style.textAlign = 'right';
                if (input.type === 'tel' || input.type === 'number') {
                    input.style.direction = 'ltr';
                }
            });

            // Fix tables for RTL
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                table.style.direction = 'rtl';
                const ths = table.querySelectorAll('th');
                const tds = table.querySelectorAll('td');
                ths.forEach(th => th.style.textAlign = 'right');
                tds.forEach(td => td.style.textAlign = 'right');
            });

            // Fix lists for RTL
            const lists = document.querySelectorAll('ul, ol');
            lists.forEach(list => {
                list.style.direction = 'rtl';
                list.style.textAlign = 'right';
            });

            // Fix progress bars for RTL
            const progressBars = document.querySelectorAll('.progress-bar');
            progressBars.forEach(bar => {
                bar.style.transform = 'rotate(180deg)';
            });
        }
    }

    // Update content for RTL
    updateContentForRTL() {
        if (this.currentLang === 'ar') {
            // Update cart text
            const cartToggleBtn = document.querySelector('.cart-toggle-btn');
            if (cartToggleBtn) {
                const badge = cartToggleBtn.querySelector('.badge');
                if (badge) {
                    badge.style.marginRight = '0.5rem';
                    badge.style.marginLeft = '0';
                }
            }

            // Update buttons with icons
            const iconButtons = document.querySelectorAll('[class*="me-"], [class*="ms-"]');
            iconButtons.forEach(btn => {
                const icon = btn.querySelector('i');
                if (icon) {
                    // Swap margin classes for RTL
                    if (btn.classList.contains('me-2')) {
                        btn.classList.remove('me-2');
                        btn.classList.add('ms-2');
                    } else if (btn.classList.contains('ms-2')) {
                        btn.classList.remove('ms-2');
                        btn.classList.add('me-2');
                    }
                }
            });
        }
    }

    // Fix carousel for RTL
    fixCarouselRTL() {
        if (this.currentLang === 'ar') {
            const carousels = document.querySelectorAll('.carousel');
            carousels.forEach(carousel => {
                // Reverse carousel direction for RTL
                const prevBtn = carousel.querySelector('.carousel-control-prev');
                const nextBtn = carousel.querySelector('.carousel-control-next');
                
                if (prevBtn && nextBtn) {
                    // Swap positions
                    prevBtn.style.right = '0';
                    prevBtn.style.left = 'auto';
                    nextBtn.style.left = '0';
                    nextBtn.style.right = 'auto';
                }
            });
        }
    }

    // Fix tooltips for RTL
    fixTooltipsRTL() {
        if (this.currentLang === 'ar') {
            const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
            tooltips.forEach(tooltip => {
                tooltip.setAttribute('data-bs-placement', 'left');
            });
        }
    }

    // Update date/time formatting for RTL
    updateDateTimeRTL() {
        if (this.currentLang === 'ar') {
            // Use Arabic date format
            const dateElements = document.querySelectorAll('.date, .time');
            dateElements.forEach(el => {
                // This would integrate with a date formatting library
                // For now, just ensure proper direction
                el.style.direction = 'rtl';
            });
        }
    }

    // Initialize all RTL fixes
    init() {
        this.adjustLayoutForRTL();
        this.updateContentForRTL();
        this.fixCarouselRTL();
        this.fixTooltipsRTL();
        this.updateDateTimeRTL();
        this.setupRTLAnimations();
    }
}

// Initialize RTL support
let rtlSupport;

document.addEventListener('DOMContentLoaded', () => {
    rtlSupport = new RTLSupport();
    
    // Re-initialize when content changes (for dynamic content)
    const observer = new MutationObserver(() => {
        rtlSupport.init();
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});

// Export for global access
window.RTLSupport = RTLSupport;
window.rtlSupport = rtlSupport;

// Global functions for language switching
window.switchLanguage = (lang) => {
    if (rtlSupport) {
        rtlSupport.switchLanguage(lang);
    }
};

window.updateRTLLayout = () => {
    if (rtlSupport) {
        rtlSupport.init();
    }
};
