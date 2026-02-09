// Advanced Checkout System

class CheckoutManager {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 3;
        this.orderData = {
            items: [],
            customer: {},
            delivery: {},
            payment: {},
            totals: {}
        };
        this.init();
    }

    init() {
        this.loadCartFromStorage();
        this.setupEventListeners();
        this.updateOrderSummary();
        this.updateProgressSteps();
    }

    loadCartFromStorage() {
        const cartData = sessionStorage.getItem('checkoutCart');
        if (cartData) {
            this.orderData.items = JSON.parse(cartData);
        } else {
            // Redirect to cart if no items
            this.showNotification('No items in cart. Redirecting...', 'warning');
            setTimeout(() => window.location.href = '/menu/', 2000);
        }
    }

    setupEventListeners() {
        // Order type change
        document.querySelectorAll('input[name="order_type"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.toggleDeliveryFields(e.target.value === 'delivery');
            });
        });

        // Payment method change
        document.querySelectorAll('input[name="payment_method"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.showPaymentForm(e.target.value);
            });
        });

        // Card number formatting
        const cardNumberInput = document.getElementById('card_number');
        if (cardNumberInput) {
            cardNumberInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\s/g, '');
                let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
                e.target.value = formattedValue;
            });
        }

        // Card expiry formatting
        const cardExpiryInput = document.getElementById('card_expiry');
        if (cardExpiryInput) {
            cardExpiryInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length >= 2) {
                    value = value.slice(0, 2) + '/' + value.slice(2, 4);
                }
                e.target.value = value;
            });
        }

        // CVV validation
        const cardCvvInput = document.getElementById('card_cvv');
        if (cardCvvInput) {
            cardCvvInput.addEventListener('input', (e) => {
                e.target.value = e.target.value.replace(/\D/g, '').slice(0, 3);
            });
        }

        // Form validation
        document.querySelectorAll('.form-control, .form-select').forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
        });

        // Promo code
        const applyPromoBtn = document.getElementById('apply-promo');
        if (applyPromoBtn) {
            applyPromoBtn.addEventListener('click', () => this.applyPromoCode());
        }
    }

    toggleDeliveryFields(showDelivery) {
        const deliveryFields = document.querySelector('.delivery-address');
        if (deliveryFields) {
            deliveryFields.style.display = showDelivery ? 'block' : 'none';
        }
        
        // Update delivery time options
        const deliveryTimeSelect = document.getElementById('delivery_time');
        if (deliveryTimeSelect) {
            if (showDelivery) {
                deliveryTimeSelect.innerHTML = `
                    <option value="asap">ASAP (25-35 min)</option>
                    <option value="30min">30 minutes</option>
                    <option value="45min">45 minutes</option>
                    <option value="1hour">1 hour</option>
                    <option value="schedule">Schedule for later</option>
                `;
            } else {
                deliveryTimeSelect.innerHTML = `
                    <option value="15min">15 minutes</option>
                    <option value="20min">20 minutes</option>
                    <option value="25min">25 minutes</option>
                    <option value="30min">30 minutes</option>
                `;
            }
        }
    }

    showPaymentForm(method) {
        // Hide all payment forms
        document.querySelectorAll('.payment-form').forEach(form => {
            form.style.display = 'none';
        });

        // Show selected payment form
        const selectedForm = document.getElementById(`${method}-form`);
        if (selectedForm) {
            selectedForm.style.display = 'block';
        }

        // Update payment method selection UI
        document.querySelectorAll('.payment-method').forEach(methodEl => {
            methodEl.classList.remove('active');
        });
        document.querySelector(`[data-method="${method}"]`)?.classList.add('active');
    }

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Remove previous validation classes
        field.classList.remove('is-invalid', 'is-valid');

        // Validation rules
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'This field is required';
        } else if (field.type === 'email' && value && !this.isValidEmail(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address';
        } else if (field.type === 'tel' && value && !this.isValidPhone(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid phone number';
        } else if (field.id === 'card_number' && value && value.replace(/\s/g, '').length !== 16) {
            isValid = false;
            errorMessage = 'Card number must be 16 digits';
        } else if (field.id === 'card_expiry' && value && !/^\d{2}\/\d{2}$/.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid expiry date (MM/YY)';
        } else if (field.id === 'card_cvv' && value && value.length !== 3) {
            isValid = false;
            errorMessage = 'CVV must be 3 digits';
        }

        // Add validation classes and feedback
        if (!isValid) {
            field.classList.add('is-invalid');
            this.showFieldError(field, errorMessage);
        } else if (value) {
            field.classList.add('is-valid');
            this.hideFieldError(field);
        }

        return isValid;
    }

    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    isValidPhone(phone) {
        return /^[\d\s\-\+\(\)]+$/.test(phone) && phone.replace(/\D/g, '').length >= 10;
    }

    showFieldError(field, message) {
        let feedback = field.parentNode.querySelector('.invalid-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            field.parentNode.appendChild(feedback);
        }
        feedback.textContent = message;
    }

    hideFieldError(field) {
        const feedback = field.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.remove();
        }
    }

    validateStep(step) {
        let isValid = true;
        const stepElement = document.getElementById(`step-${step}`);
        
        if (!stepElement) return false;

        // Validate all required fields in current step
        const requiredFields = stepElement.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        // Additional step-specific validations
        if (step === 2) {
            const paymentMethod = document.querySelector('input[name="payment_method"]:checked')?.value;
            if (!paymentMethod) {
                this.showNotification('Please select a payment method', 'error');
                return false;
            }

            if (paymentMethod === 'card') {
                const cardFields = ['card_number', 'card_expiry', 'card_cvv', 'card_name'];
                cardFields.forEach(fieldId => {
                    const field = document.getElementById(fieldId);
                    if (field && !this.validateField(field)) {
                        isValid = false;
                    }
                });
            }
        }

        if (step === 3) {
            const termsAccepted = document.getElementById('terms_accepted')?.checked;
            if (!termsAccepted) {
                this.showNotification('Please accept the terms and conditions', 'error');
                return false;
            }
        }

        return isValid;
    }

    collectStepData(step) {
        const stepElement = document.getElementById(`step-${step}`);
        const formData = {};

        if (step === 1) {
            // Delivery information
            const orderType = document.querySelector('input[name="order_type"]:checked')?.value || 'delivery';
            formData.order_type = orderType;
            
            if (orderType === 'delivery') {
                formData.first_name = document.getElementById('first_name')?.value;
                formData.last_name = document.getElementById('last_name')?.value;
                formData.email = document.getElementById('email')?.value;
                formData.phone = document.getElementById('phone')?.value;
                formData.address = document.getElementById('address')?.value;
                formData.city = document.getElementById('city')?.value;
                formData.postal_code = document.getElementById('postal_code')?.value;
                formData.country = document.getElementById('country')?.value;
                formData.delivery_instructions = document.getElementById('delivery_instructions')?.value;
            }
            formData.delivery_time = document.getElementById('delivery_time')?.value;
            
            this.orderData.delivery = formData;
        } else if (step === 2) {
            // Payment information
            const paymentMethod = document.querySelector('input[name="payment_method"]:checked')?.value;
            formData.payment_method = paymentMethod;
            
            if (paymentMethod === 'card') {
                formData.card_number = document.getElementById('card_number')?.value;
                formData.card_expiry = document.getElementById('card_expiry')?.value;
                formData.card_name = document.getElementById('card_name')?.value;
                // Don't store CVV in order data for security
            }
            
            this.orderData.payment = formData;
        }

        return formData;
    }

    updateProgressSteps() {
        document.querySelectorAll('.step').forEach((step, index) => {
            const stepNumber = index + 1;
            step.classList.remove('active', 'completed');
            
            if (stepNumber === this.currentStep) {
                step.classList.add('active');
            } else if (stepNumber < this.currentStep) {
                step.classList.add('completed');
            }
        });
    }

    updateOrderSummary() {
        // Calculate totals
        const subtotal = this.orderData.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        const tax = subtotal * 0.1;
        const delivery = subtotal > 20 ? 0 : 2.99;
        const total = subtotal + tax + delivery;

        this.orderData.totals = { subtotal, tax, delivery, total };

        // Update sidebar summary
        this.updateSidebarSummary();
        
        // Update review step summary (if on step 3)
        if (this.currentStep === 3) {
            this.updateReviewSummary();
        }
    }

    updateSidebarSummary() {
        // Update items
        const sidebarItems = document.getElementById('sidebar-items');
        if (sidebarItems) {
            sidebarItems.innerHTML = this.orderData.items.map(item => `
                <div class="sidebar-item">
                    <div class="sidebar-item-details">
                        <div class="sidebar-item-name">${item.name}</div>
                        <div class="sidebar-item-quantity">Qty: ${item.quantity}</div>
                    </div>
                    <div class="sidebar-item-price">${(item.price * item.quantity).toFixed(2)} €</div>
                </div>
            `).join('');
        }

        // Update totals
        const totals = this.orderData.totals;
        document.getElementById('sidebar-subtotal').textContent = `${totals.subtotal.toFixed(2)} €`;
        document.getElementById('sidebar-tax').textContent = `${totals.tax.toFixed(2)} €`;
        document.getElementById('sidebar-delivery').textContent = totals.delivery === 0 ? 'FREE' : `${totals.delivery.toFixed(2)} €`;
        document.getElementById('sidebar-total').textContent = `${totals.total.toFixed(2)} €`;
    }

    updateReviewSummary() {
        // Update items
        const reviewItems = document.getElementById('review-items');
        if (reviewItems) {
            reviewItems.innerHTML = this.orderData.items.map(item => `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <div>
                        <div class="fw-medium">${item.name}</div>
                        <small class="text-muted">Quantity: ${item.quantity}</small>
                    </div>
                    <span>${(item.price * item.quantity).toFixed(2)} €</span>
                </div>
            `).join('');
        }

        // Update totals
        const totals = this.orderData.totals;
        document.getElementById('review-subtotal').textContent = `${totals.subtotal.toFixed(2)} €`;
        document.getElementById('review-tax').textContent = `${totals.tax.toFixed(2)} €`;
        document.getElementById('review-delivery').textContent = totals.delivery === 0 ? 'FREE' : `${totals.delivery.toFixed(2)} €`;
        document.getElementById('review-total').textContent = `${totals.total.toFixed(2)} €`;

        // Update delivery info
        const deliveryInfo = document.getElementById('review-delivery-info');
        if (deliveryInfo && this.orderData.delivery) {
            const delivery = this.orderData.delivery;
            deliveryInfo.innerHTML = `
                <div class="mb-2">
                    <strong>${delivery.first_name} ${delivery.last_name}</strong>
                </div>
                <div class="mb-2">${delivery.email}</div>
                <div class="mb-2">${delivery.phone}</div>
                ${delivery.address ? `
                    <div class="mb-2">
                        ${delivery.address}<br>
                        ${delivery.city}, ${delivery.postal_code}<br>
                        ${delivery.country}
                    </div>
                ` : ''}
                <div class="mb-2">
                    <strong>Order Type:</strong> ${delivery.order_type === 'delivery' ? 'Delivery' : 'Pickup'}
                </div>
                <div>
                    <strong>Time:</strong> ${delivery.delivery_time === 'asap' ? 'ASAP' : delivery.delivery_time}
                </div>
            `;
        }

        // Update payment info
        const paymentInfo = document.getElementById('review-payment-info');
        if (paymentInfo && this.orderData.payment) {
            const payment = this.orderData.payment;
            const paymentMethods = {
                'card': 'Credit/Debit Card',
                'paypal': 'PayPal',
                'cash': 'Cash on Delivery'
            };
            paymentInfo.innerHTML = `
                <div class="d-flex align-items-center">
                    <i class="fas fa-${payment.payment_method === 'card' ? 'credit-card' : payment.payment_method === 'paypal' ? 'paypal' : 'money-bill-wave'} me-2"></i>
                    <span>${paymentMethods[payment.payment_method] || payment.payment_method}</span>
                </div>
            `;
        }
    }

    applyPromoCode() {
        const promoInput = document.getElementById('promo_code');
        const promoCode = promoInput?.value.trim();
        
        if (!promoCode) {
            this.showNotification('Please enter a promo code', 'warning');
            return;
        }

        // Simulate promo code validation (in real app, this would be an API call)
        const validPromos = {
            'SAVE10': 0.1,
            'SAVE20': 0.2,
            'WELCOME': 0.15
        };

        if (validPromos[promoCode]) {
            this.showNotification(`Promo code applied! You saved ${validPromos[promoCode] * 100}%`, 'success');
            promoInput.disabled = true;
            document.getElementById('apply-promo').textContent = 'Applied';
            document.getElementById('apply-promo').disabled = true;
            
            // Recalculate totals with discount
            this.updateOrderSummary();
        } else {
            this.showNotification('Invalid promo code', 'error');
        }
    }

    placeOrder() {
        if (!this.validateStep(3)) {
            return;
        }

        // Show loading state
        const placeOrderBtn = document.getElementById('place-order-btn');
        const originalText = placeOrderBtn.innerHTML;
        placeOrderBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Placing Order...';
        placeOrderBtn.disabled = true;

        // Simulate order processing
        setTimeout(() => {
            // Generate order number
            const orderNumber = 'ORD' + Date.now();
            
            // Save order to localStorage (in real app, this would be sent to server)
            const order = {
                ...this.orderData,
                orderNumber: orderNumber,
                status: 'confirmed',
                createdAt: new Date().toISOString()
            };
            
            localStorage.setItem(`order_${orderNumber}`, JSON.stringify(order));
            
            // Clear cart
            localStorage.removeItem('cart');
            sessionStorage.removeItem('checkoutCart');
            
            // Show success message
            this.showOrderConfirmation(order);
            
            // Redirect to order confirmation page
            setTimeout(() => {
                window.location.href = `/order-confirmation/${orderNumber}/`;
            }, 3000);
        }, 2000);
    }

    showOrderConfirmation(order) {
        const confirmationHTML = `
            <div class="order-confirmation-overlay">
                <div class="order-confirmation-modal">
                    <div class="text-center">
                        <div class="success-icon mb-3">
                            <i class="fas fa-check-circle fa-4x text-success"></i>
                        </div>
                        <h3>Order Confirmed!</h3>
                        <p class="text-muted">Your order has been placed successfully.</p>
                        <div class="order-number mb-3">
                            <strong>Order Number:</strong> ${order.orderNumber}
                        </div>
                        <div class="estimated-time mb-3">
                            <i class="fas fa-clock me-2"></i>
                            Estimated delivery: 25-35 minutes
                        </div>
                        <button class="btn btn-primary" onclick="window.location.href='/order-tracking/${order.orderNumber}/'">
                            Track Order
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', confirmationHTML);
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
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }
}

// Global functions for navigation
function goToStep(step) {
    if (!checkoutManager.validateStep(checkoutManager.currentStep)) {
        return;
    }
    
    // Collect current step data
    checkoutManager.collectStepData(checkoutManager.currentStep);
    
    // Hide current step
    document.getElementById(`step-${checkoutManager.currentStep}`).classList.remove('active');
    
    // Show new step
    checkoutManager.currentStep = step;
    document.getElementById(`step-${step}`).classList.add('active');
    
    // Update progress
    checkoutManager.updateProgressSteps();
    
    // Update review summary if going to step 3
    if (step === 3) {
        checkoutManager.updateReviewSummary();
    }
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function goBack() {
    window.history.back();
}

// Initialize checkout manager
let checkoutManager;

document.addEventListener('DOMContentLoaded', () => {
    checkoutManager = new CheckoutManager();
});
