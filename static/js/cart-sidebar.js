/**
 * 60 SECONDS TO NAPOLI - Cart Sidebar Component
 * Handles cart sidebar UI and interactions
 */

(function() {
    'use strict';

    const CartSidebar = {
        elements: {
            sidebar: null,
            overlay: null,
            toggleBtn: null,
            closeBtn: null,
            itemsContainer: null,
            emptyState: null,
            subtotal: null,
            checkoutBtn: null
        },

        init() {
            this.cacheElements();
            this.bindEvents();
            this.render();

            // Listen for cart changes
            if (window.Napoli && Napoli.cart) {
                Napoli.cart.onChange(() => this.render());
            }
        },

        cacheElements() {
            this.elements.sidebar = document.getElementById('cart-sidebar');
            this.elements.overlay = document.getElementById('cart-overlay');
            this.elements.toggleBtn = document.getElementById('cart-toggle-btn');
            this.elements.closeBtn = document.getElementById('cart-close-btn');
            this.elements.itemsContainer = document.getElementById('cart-items-container');
            this.elements.emptyState = document.getElementById('cart-empty-state');
            this.elements.subtotal = document.getElementById('cart-subtotal');
            this.elements.checkoutBtn = document.getElementById('checkout-btn');
        },

        bindEvents() {
            if (this.elements.toggleBtn) {
                this.elements.toggleBtn.addEventListener('click', () => this.open());
            }

            if (this.elements.closeBtn) {
                this.elements.closeBtn.addEventListener('click', () => this.close());
            }

            if (this.elements.overlay) {
                this.elements.overlay.addEventListener('click', () => this.close());
            }

            // Close on escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.isOpen()) {
                    this.close();
                }
            });

            // Delegate events for cart item actions
            if (this.elements.itemsContainer) {
                this.elements.itemsContainer.addEventListener('click', (e) => {
                    const target = e.target.closest('[data-action]');
                    if (!target) return;

                    const action = target.dataset.action;
                    const itemId = parseInt(target.dataset.itemId);

                    switch (action) {
                        case 'increase':
                            this.updateQuantity(itemId, 1);
                            break;
                        case 'decrease':
                            this.updateQuantity(itemId, -1);
                            break;
                        case 'remove':
                            this.removeItem(itemId);
                            break;
                    }
                });
            }
        },

        open() {
            if (this.elements.sidebar) {
                this.elements.sidebar.classList.add('open');
                document.body.style.overflow = 'hidden';
            }
            if (this.elements.overlay) {
                this.elements.overlay.classList.add('visible');
            }
        },

        close() {
            if (this.elements.sidebar) {
                this.elements.sidebar.classList.remove('open');
                document.body.style.overflow = '';
            }
            if (this.elements.overlay) {
                this.elements.overlay.classList.remove('visible');
            }
        },

        isOpen() {
            return this.elements.sidebar && this.elements.sidebar.classList.contains('open');
        },

        render() {
            if (!window.Napoli || !Napoli.cart) return;

            const items = Napoli.cart.items;
            const isEmpty = items.length === 0;

            // Show/hide empty state
            if (this.elements.emptyState) {
                this.elements.emptyState.style.display = isEmpty ? 'block' : 'none';
            }

            // Render items
            if (!isEmpty) {
                const itemsHtml = items.map(item => this.renderItem(item)).join('');
                
                // Find or create items list
                let itemsList = this.elements.itemsContainer.querySelector('.cart-items-list');
                if (!itemsList) {
                    itemsList = document.createElement('div');
                    itemsList.className = 'cart-items-list';
                    this.elements.itemsContainer.insertBefore(itemsList, this.elements.emptyState);
                }
                itemsList.innerHTML = itemsHtml;
            } else {
                const itemsList = this.elements.itemsContainer.querySelector('.cart-items-list');
                if (itemsList) {
                    itemsList.remove();
                }
            }

            // Update subtotal
            if (this.elements.subtotal) {
                this.elements.subtotal.textContent = Napoli.utils.formatCurrency(Napoli.cart.getTotal());
            }

            // Update checkout button state
            if (this.elements.checkoutBtn) {
                if (isEmpty) {
                    this.elements.checkoutBtn.classList.add('disabled');
                    this.elements.checkoutBtn.setAttribute('tabindex', '-1');
                } else {
                    this.elements.checkoutBtn.classList.remove('disabled');
                    this.elements.checkoutBtn.removeAttribute('tabindex');
                }
            }
        },

        renderItem(item) {
            const itemTotal = parseFloat(item.price) * item.quantity;
            const imageUrl = item.image || '/static/images/placeholder-food.jpg';
            
            return `
                <div class="cart-item" data-item-id="${item.id}">
                    <img src="${imageUrl}" alt="${item.name}" class="cart-item-image">
                    <div class="cart-item-details">
                        <div class="cart-item-name">${item.name}</div>
                        <div class="cart-item-price">${Napoli.utils.formatCurrency(itemTotal)}</div>
                        <div class="cart-item-quantity mt-2">
                            <button class="btn-qty" data-action="decrease" data-item-id="${item.id}" aria-label="Decrease quantity">
                                <i class="fas fa-minus"></i>
                            </button>
                            <span class="qty-value">${item.quantity}</span>
                            <button class="btn-qty" data-action="increase" data-item-id="${item.id}" aria-label="Increase quantity">
                                <i class="fas fa-plus"></i>
                            </button>
                        </div>
                    </div>
                    <button class="btn btn-link text-danger p-0" data-action="remove" data-item-id="${item.id}" aria-label="Remove item">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            `;
        },

        updateQuantity(itemId, delta) {
            if (!window.Napoli || !Napoli.cart) return;

            const item = Napoli.cart.items.find(i => i.id === itemId);
            if (item) {
                const newQuantity = item.quantity + delta;
                Napoli.cart.updateQuantity(itemId, newQuantity);
            }
        },

        removeItem(itemId) {
            if (!window.Napoli || !Napoli.cart) return;

            const item = Napoli.cart.items.find(i => i.id === itemId);
            if (item) {
                Napoli.cart.remove(itemId);
                Napoli.toast.info(`${item.name} removed from cart`);
            }
        }
    };

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', () => {
        CartSidebar.init();
    });

    // Export to global
    window.CartSidebar = CartSidebar;
})();
