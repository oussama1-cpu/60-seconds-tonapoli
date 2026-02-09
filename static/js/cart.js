// Advanced Cart Management System

class CartManager {
    constructor() {
        this.cart = JSON.parse(localStorage.getItem('cart')) || [];
        this.isCartOpen = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateCartUI();
        this.createCartSidebar();
        this.loadCartFromStorage();
    }

    setupEventListeners() {
        // Cart toggle buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('.add-to-cart-btn, [data-action="add-to-cart"]')) {
                e.preventDefault();
                const itemId = e.target.dataset.itemId || e.target.closest('[data-item-id]').dataset.itemId;
                this.addToCart(itemId);
            }
        });

        // Cart sidebar controls
        document.addEventListener('click', (e) => {
            if (e.target.matches('#close-cart, .cart-overlay')) {
                this.closeCartSidebar();
            }
            if (e.target.matches('#continue-shopping')) {
                this.closeCartSidebar();
            }
            if (e.target.matches('#checkout-btn')) {
                this.proceedToCheckout();
            }
        });
    }

    createCartSidebar() {
        // Check if cart sidebar already exists
        if (document.getElementById('cart-sidebar')) {
            return;
        }

        // Create cart sidebar HTML
        const cartHTML = `
            <div id="cart-sidebar" class="cart-sidebar">
                <div class="cart-header">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">
                            <i class="fas fa-shopping-cart me-2"></i>
                            Your Cart
                            <span class="badge bg-primary ms-2" id="cart-count">0</span>
                        </h5>
                        <button class="btn btn-sm btn-outline-secondary" id="close-cart">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>

                <div class="cart-body">
                    <div id="empty-cart" class="text-center py-5">
                        <i class="fas fa-shopping-cart fa-3x text-muted mb-3"></i>
                        <h6 class="text-muted">Your cart is empty</h6>
                        <p class="small text-muted">Add delicious items to get started!</p>
                        <button class="btn btn-primary btn-sm" onclick="cartManager.closeCartSidebar()">
                            <i class="fas fa-utensils me-2"></i>Browse Menu
                        </button>
                    </div>

                    <div id="cart-items" class="cart-items" style="display: none;"></div>

                    <div id="cart-summary" class="cart-summary" style="display: none;">
                        <div class="border-top pt-3">
                            <div class="d-flex justify-content-between mb-2">
                                <span>Subtotal:</span>
                                <span id="cart-subtotal">0.00 €</span>
                            </div>
                            <div class="d-flex justify-content-between mb-2">
                                <span>Tax (10%):</span>
                                <span id="cart-tax">0.00 €</span>
                            </div>
                            <div class="d-flex justify-content-between mb-2">
                                <span>Delivery:</span>
                                <span id="cart-delivery">FREE</span>
                            </div>
                            <div class="d-flex justify-content-between fw-bold fs-5">
                                <span>Total:</span>
                                <span id="cart-total">0.00 €</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="cart-footer">
                    <div id="cart-actions" style="display: none;">
                        <div class="d-grid gap-2">
                            <button class="btn btn-primary" id="checkout-btn">
                                <i class="fas fa-credit-card me-2"></i>
                                Proceed to Checkout
                            </button>
                            <button class="btn btn-outline-secondary" id="continue-shopping">
                                <i class="fas fa-arrow-left me-2"></i>
                                Continue Shopping
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div id="cart-overlay" class="cart-overlay"></div>
        `;

        document.body.insertAdjacentHTML('beforeend', cartHTML);
    }

    addToCart(itemId, quantity = 1, customizations = {}) {
        // Find item data (this would typically come from your API)
        const itemElement = document.querySelector(`[data-item-id="${itemId}"]`);
        if (!itemElement) {
            this.showNotification('Item not found', 'error');
            return;
        }

        const itemName = itemElement.querySelector('.card-title, .menu-item-title')?.textContent || 'Unknown Item';
        const itemPrice = parseFloat(itemElement.dataset.itemPrice || itemElement.querySelector('.text-primary, .badge')?.textContent.replace('€', '').trim() || 0);
        const itemImage = itemElement.querySelector('.menu-item-img')?.src || '';

        // Check if item already exists in cart
        const existingItem = this.cart.find(item => item.id === itemId && JSON.stringify(item.customizations) === JSON.stringify(customizations));
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.cart.push({
                id: itemId,
                name: itemName,
                price: itemPrice,
                image: itemImage,
                quantity: quantity,
                customizations: customizations
            });
        }

        this.saveCart();
        this.updateCartUI();
        this.showNotification(`${itemName} added to cart!`, 'success');
        this.openCartSidebar();
    }

    removeFromCart(itemId, customizations = {}) {
        this.cart = this.cart.filter(item => !(item.id === itemId && JSON.stringify(item.customizations) === JSON.stringify(customizations)));
        this.saveCart();
        this.updateCartUI();
        this.showNotification('Item removed from cart', 'info');
    }

    updateQuantity(itemId, quantity, customizations = {}) {
        const item = this.cart.find(item => item.id === itemId && JSON.stringify(item.customizations) === JSON.stringify(customizations));
        if (item) {
            if (quantity <= 0) {
                this.removeFromCart(itemId, customizations);
            } else {
                item.quantity = quantity;
                this.saveCart();
                this.updateCartUI();
            }
        }
    }

    clearCart() {
        this.cart = [];
        this.saveCart();
        this.updateCartUI();
        this.showNotification('Cart cleared', 'info');
    }

    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.cart));
    }

    loadCartFromStorage() {
        this.cart = JSON.parse(localStorage.getItem('cart')) || [];
        this.updateCartUI();
    }

    updateCartUI() {
        const cartCount = document.getElementById('cart-count');
        const emptyCart = document.getElementById('empty-cart');
        const cartItems = document.getElementById('cart-items');
        const cartSummary = document.getElementById('cart-summary');
        const cartActions = document.getElementById('cart-actions');

        const totalItems = this.cart.reduce((sum, item) => sum + item.quantity, 0);
        
        // Update cart count badge
        if (cartCount) {
            cartCount.textContent = totalItems;
            cartCount.classList.add('cart-badge-update');
            setTimeout(() => cartCount.classList.remove('cart-badge-update'), 300);
        }

        // Update global cart count (if exists)
        const globalCartCount = document.querySelector('.fa-shopping-cart').nextElementSibling;
        if (globalCartCount && globalCartCount.classList.contains('badge')) {
            globalCartCount.textContent = totalItems;
        }

        // Show/hide appropriate sections
        if (this.cart.length === 0) {
            emptyCart.style.display = 'block';
            cartItems.style.display = 'none';
            cartSummary.style.display = 'none';
            cartActions.style.display = 'none';
        } else {
            emptyCart.style.display = 'none';
            cartItems.style.display = 'block';
            cartSummary.style.display = 'block';
            cartActions.style.display = 'block';
            
            this.renderCartItems();
            this.updateCartSummary();
        }
    }

    renderCartItems() {
        const cartItemsContainer = document.getElementById('cart-items');
        if (!cartItemsContainer) return;

        cartItemsContainer.innerHTML = this.cart.map((item, index) => `
            <div class="cart-item" data-cart-index="${index}">
                <div class="cart-item-image">
                    ${item.image ? `<img src="${item.image}" alt="${item.name}">` : '<div class="cart-item-placeholder"><i class="fas fa-utensils"></i></div>'}
                </div>
                <div class="cart-item-details">
                    <div class="cart-item-name">${item.name}</div>
                    ${Object.keys(item.customizations).length > 0 ? 
                        `<div class="cart-item-customizations">${this.formatCustomizations(item.customizations)}</div>` : ''}
                    <div class="cart-item-price">${item.price.toFixed(2)} €</div>
                </div>
                <div class="cart-item-quantity">
                    <button class="quantity-btn" onclick="cartManager.updateQuantity('${item.id}', ${item.quantity - 1}, ${JSON.stringify(item.customizations).replace(/"/g, '&quot;')})">
                        <i class="fas fa-minus"></i>
                    </button>
                    <input type="number" class="quantity-input" value="${item.quantity}" min="1" max="10" 
                           onchange="cartManager.updateQuantity('${item.id}', parseInt(this.value), ${JSON.stringify(item.customizations).replace(/"/g, '&quot;')})">
                    <button class="quantity-btn" onclick="cartManager.updateQuantity('${item.id}', ${item.quantity + 1}, ${JSON.stringify(item.customizations).replace(/"/g, '&quot;')})">
                        <i class="fas fa-plus"></i>
                    </button>
                </div>
                <button class="btn btn-sm btn-outline-danger ms-2" onclick="cartManager.removeFromCart('${item.id}', ${JSON.stringify(item.customizations).replace(/"/g, '&quot;')})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `).join('');
    }

    formatCustomizations(customizations) {
        return Object.entries(customizations)
            .map(([key, value]) => `${key}: ${value}`)
            .join(', ');
    }

    updateCartSummary() {
        const subtotal = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        const tax = subtotal * 0.1; // 10% tax
        const delivery = subtotal > 20 ? 0 : 2.99; // Free delivery over 20€
        const total = subtotal + tax + delivery;

        // Update summary elements
        document.getElementById('cart-subtotal').textContent = `${subtotal.toFixed(2)} €`;
        document.getElementById('cart-tax').textContent = `${tax.toFixed(2)} €`;
        document.getElementById('cart-delivery').textContent = delivery === 0 ? 'FREE' : `${delivery.toFixed(2)} €`;
        document.getElementById('cart-total').textContent = `${total.toFixed(2)} €`;
    }

    openCartSidebar() {
        const sidebar = document.getElementById('cart-sidebar');
        const overlay = document.getElementById('cart-overlay');
        
        if (sidebar && overlay) {
            sidebar.classList.add('open');
            overlay.classList.add('show');
            this.isCartOpen = true;
        }
    }

    closeCartSidebar() {
        const sidebar = document.getElementById('cart-sidebar');
        const overlay = document.getElementById('cart-overlay');
        
        if (sidebar && overlay) {
            sidebar.classList.remove('open');
            overlay.classList.remove('show');
            this.isCartOpen = false;
        }
    }

    proceedToCheckout() {
        if (this.cart.length === 0) {
            this.showNotification('Your cart is empty', 'warning');
            return;
        }
        
        // Save cart to session storage for checkout page
        sessionStorage.setItem('checkoutCart', JSON.stringify(this.cart));
        
        // Redirect to checkout page
        window.location.href = '/checkout/';
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }

    // Get cart data for checkout
    getCartData() {
        return this.cart;
    }

    // Get cart totals
    getCartTotals() {
        const subtotal = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        const tax = subtotal * 0.1;
        const delivery = subtotal > 20 ? 0 : 2.99;
        const total = subtotal + tax + delivery;
        
        return { subtotal, tax, delivery, total };
    }
}

// Initialize cart manager
let cartManager;

document.addEventListener('DOMContentLoaded', () => {
    cartManager = new CartManager();
    
    // Add cart button to header if not exists
    const headerActions = document.querySelector('.header-actions, .navbar-nav');
    if (headerActions && !document.querySelector('.cart-toggle-btn')) {
        const cartButton = document.createElement('button');
        cartButton.className = 'btn btn-outline-primary cart-toggle-btn';
        cartButton.innerHTML = `
            <i class="fas fa-shopping-cart"></i>
            <span class="badge bg-primary ms-1">0</span>
        `;
        cartButton.onclick = () => cartManager.openCartSidebar();
        headerActions.appendChild(cartButton);
    }
});

// Global functions for cart operations
window.addToCart = (itemId, quantity = 1, customizations = {}) => {
    if (cartManager) {
        cartManager.addToCart(itemId, quantity, customizations);
    }
};

window.openCartSidebar = () => {
    if (cartManager) {
        cartManager.openCartSidebar();
    }
};

window.closeCartSidebar = () => {
    if (cartManager) {
        cartManager.closeCartSidebar();
    }
};
