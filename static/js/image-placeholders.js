// Image Placeholder System

class ImagePlaceholderManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupImageFallbacks();
        this.setupLazyLoading();
        this.setupImageErrorHandling();
    }

    setupImageFallbacks() {
        // Replace missing images with placeholders
        document.querySelectorAll('img').forEach(img => {
            if (!img.complete || img.naturalWidth === 0) {
                this.replaceWithPlaceholder(img);
            }
        });
    }

    replaceWithPlaceholder(img) {
        const placeholder = this.createPlaceholder(img);
        if (placeholder && img.parentNode) {
            img.parentNode.replaceChild(placeholder, img);
        }
    }

    createPlaceholder(originalImg) {
        const container = document.createElement('div');
        container.className = originalImg.className + ' fallback';
        
        // Determine category from context
        const category = this.getCategoryFromContext(originalImg);
        container.classList.add(`placeholder-${category}`);
        
        // Add icon based on category
        const icon = this.getCategoryIcon(category);
        container.innerHTML = `<i class="fas fa-${icon}"></i>`;
        
        // Copy styles
        const computedStyle = window.getComputedStyle(originalImg);
        container.style.width = computedStyle.width;
        container.style.height = computedStyle.height;
        container.style.display = computedStyle.display;
        
        return container;
    }

    getCategoryFromContext(img) {
        // Try to determine category from surrounding elements
        const parent = img.closest('.menu-item-wrapper, .category-section');
        if (parent) {
            const text = parent.textContent.toLowerCase();
            if (text.includes('pizza')) return 'pizza';
            if (text.includes('pasta')) return 'pasta';
            if (text.includes('salad')) return 'salad';
            if (text.includes('dessert') || text.includes('sweet')) return 'dessert';
            if (text.includes('drink') || text.includes('beverage')) return 'drink';
            if (text.includes('appetizer') || text.includes('starter')) return 'appetizer';
        }
        return 'pizza'; // default
    }

    getCategoryIcon(category) {
        const icons = {
            'pizza': 'pizza-slice',
            'pasta': 'utensils',
            'salad': 'leaf',
            'dessert': 'ice-cream',
            'drink': 'glass-water',
            'appetizer': 'cheese'
        };
        return icons[category] || 'utensils';
    }

    setupLazyLoading() {
        // Intersection Observer for lazy loading
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        this.loadImage(img);
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    loadImage(img) {
        const src = img.dataset.src;
        if (!src) return;

        img.src = src;
        img.onload = () => {
            img.classList.add('loaded');
            img.removeAttribute('data-src');
        };
        img.onerror = () => {
            this.replaceWithPlaceholder(img);
        };
    }

    setupImageErrorHandling() {
        // Global error handler for images
        document.addEventListener('error', (e) => {
            if (e.target.tagName === 'IMG') {
                this.replaceWithPlaceholder(e.target);
            }
        }, true);
    }

    // Method to add placeholder to specific element
    addPlaceholderToElement(element, type = 'menu-item') {
        if (!element) return;

        const placeholder = document.createElement('div');
        placeholder.className = `${type}-placeholder fallback placeholder-animated`;
        
        if (type === 'ingredient') {
            placeholder.innerHTML = '<i class="fas fa-leaf"></i>';
        } else {
            placeholder.innerHTML = '<i class="fas fa-utensils"></i>';
        }

        element.appendChild(placeholder);
    }

    // Method to create hero placeholder
    createHeroPlaceholder(category = 'pizza') {
        const hero = document.createElement('div');
        hero.className = `category-hero-image fallback placeholder-${category}`;
        hero.innerHTML = `<i class="fas fa-${this.getCategoryIcon(category)}"></i>`;
        return hero;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.imagePlaceholderManager = new ImagePlaceholderManager();
});

// Export for use in other scripts
window.ImagePlaceholderManager = ImagePlaceholderManager;
