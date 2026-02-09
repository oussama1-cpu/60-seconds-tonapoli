// Order Tracking System

class OrderTracker {
    constructor() {
        this.orderNumber = this.getOrderNumberFromURL();
        this.orderData = null;
        this.updateInterval = null;
        this.init();
    }

    init() {
        this.loadOrderData();
        this.setupEventListeners();
        this.startRealTimeUpdates();
    }

    getOrderNumberFromURL() {
        const pathParts = window.location.pathname.split('/');
        return pathParts[pathParts.length - 2] || '';
    }

    loadOrderData() {
        // Load order data from localStorage or API
        const storedOrder = localStorage.getItem(`order_${this.orderNumber}`);
        if (storedOrder) {
            this.orderData = JSON.parse(storedOrder);
            this.updateUI();
        } else {
            // Fallback to template data
            this.loadTemplateData();
        }
    }

    loadTemplateData() {
        // Extract data from the page (in production, this would come from API)
        const statusElement = document.querySelector('.status-badge');
        const stepsElements = document.querySelectorAll('.tracker-step');
        
        this.orderData = {
            orderNumber: this.orderNumber,
            status: statusElement?.textContent?.trim() || 'Unknown',
            currentStep: Array.from(stepsElements).findIndex(step => step.classList.contains('active')) + 1,
            estimatedTime: document.querySelector('.estimated-time')?.textContent?.trim() || '',
            steps: Array.from(stepsElements).map((step, index) => ({
                name: step.querySelector('.step-name')?.textContent || '',
                time: step.querySelector('.step-time')?.textContent || '',
                completed: step.classList.contains('completed'),
                active: step.classList.contains('active')
            }))
        };
    }

    setupEventListeners() {
        // Contact buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="call-partner"]')) {
                this.callDeliveryPartner();
            }
            if (e.target.matches('[data-action="send-message"]')) {
                this.openMessageModal();
            }
            if (e.target.matches('[data-action="reorder"]')) {
                this.reorderItems();
            }
        });

        // Refresh button
        const refreshBtn = document.getElementById('refresh-tracking');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refreshOrderStatus();
            });
        }
    }

    startRealTimeUpdates() {
        // Update order status every 30 seconds
        this.updateInterval = setInterval(() => {
            this.updateOrderStatus();
        }, 30000);
    }

    updateOrderStatus() {
        // Simulate real-time updates (in production, this would be an API call)
        if (this.orderData && this.orderData.currentStep < 4) {
            // Simulate progress
            const random = Math.random();
            if (random > 0.7) {
                this.orderData.currentStep++;
                this.updateUI();
                this.showNotification('Order status updated!', 'info');
            }
        }
    }

    updateUI() {
        if (!this.orderData) return;

        // Update status badge
        const statusBadge = document.querySelector('.status-badge');
        if (statusBadge) {
            statusBadge.className = `status-badge status-${this.orderData.status.toLowerCase().replace(' ', '-')}`;
            statusBadge.innerHTML = `
                <i class="fas fa-circle me-2"></i>
                ${this.orderData.status}
            `;
        }

        // Update progress tracker
        this.updateProgressTracker();

        // Update estimated time
        this.updateEstimatedTime();

        // Save to localStorage
        localStorage.setItem(`order_${this.orderNumber}`, JSON.stringify(this.orderData));
    }

    updateProgressTracker() {
        const steps = document.querySelectorAll('.tracker-step');
        const progressLine = document.querySelector('.tracker-progress');
        
        steps.forEach((step, index) => {
            const stepNumber = index + 1;
            step.classList.remove('completed', 'active');
            
            if (stepNumber < this.orderData.currentStep) {
                step.classList.add('completed');
                const icon = step.querySelector('.step-icon i');
                if (icon) {
                    icon.className = 'fas fa-check';
                }
            } else if (stepNumber === this.orderData.currentStep) {
                step.classList.add('active');
            }
        });

        // Update progress line
        if (progressLine) {
            const progressWidth = ((this.orderData.currentStep - 1) / 3) * 100;
            progressLine.style.width = `${progressWidth}%`;
        }
    }

    updateEstimatedTime() {
        const estimatedTimeElement = document.querySelector('.estimated-time');
        if (estimatedTimeElement && this.orderData.estimatedTime) {
            estimatedTimeElement.innerHTML = `
                <i class="fas fa-clock me-2"></i>
                ${this.orderData.estimatedTime}
            `;
        }
    }

    callDeliveryPartner() {
        // Simulate calling delivery partner
        this.showNotification('Calling delivery partner...', 'info');
        
        // In production, this would initiate a phone call
        setTimeout(() => {
            this.showNotification('Delivery partner contacted!', 'success');
        }, 2000);
    }

    openMessageModal() {
        // Create message modal
        const modalHTML = `
            <div class="modal fade" id="messageModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Send Message to Delivery Partner</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="mb-3">
                                <label class="form-label">Message</label>
                                <textarea class="form-control" id="delivery-message" rows="3" placeholder="Enter your message here..."></textarea>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-primary" onclick="orderTracker.sendMessage()">Send Message</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        const modal = new bootstrap.Modal(document.getElementById('messageModal'));
        modal.show();
    }

    sendMessage() {
        const messageInput = document.getElementById('delivery-message');
        const message = messageInput.value.trim();
        
        if (!message) {
            this.showNotification('Please enter a message', 'warning');
            return;
        }

        // Simulate sending message
        this.showNotification('Message sent to delivery partner!', 'success');
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('messageModal'));
        modal.hide();
        
        // Remove modal from DOM
        setTimeout(() => {
            document.getElementById('messageModal')?.remove();
        }, 500);
    }

    reorderItems() {
        // Get order items and add them to cart
        if (this.orderData && this.orderData.items) {
            this.orderData.items.forEach(item => {
                // Add to cart using cart manager
                if (window.cartManager) {
                    window.cartManager.addToCart(item.id, item.quantity, item.customizations || {});
                }
            });
            
            this.showNotification('Items added to cart!', 'success');
            
            // Redirect to cart after a delay
            setTimeout(() => {
                window.location.href = '/menu/';
            }, 2000);
        }
    }

    refreshOrderStatus() {
        // Show loading state
        const refreshBtn = document.getElementById('refresh-tracking');
        if (refreshBtn) {
            refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            refreshBtn.disabled = true;
        }

        // Simulate API call
        setTimeout(() => {
            this.updateOrderStatus();
            
            if (refreshBtn) {
                refreshBtn.innerHTML = '<i class="fas fa-sync"></i>';
                refreshBtn.disabled = false;
            }
            
            this.showNotification('Order status refreshed!', 'success');
        }, 1500);
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

    // Simulate map tracking
    initializeMap() {
        const mapContainer = document.querySelector('.map-container');
        if (mapContainer) {
            // In production, this would initialize a real map (Google Maps, etc.)
            mapContainer.innerHTML = `
                <div class="map-placeholder">
                    <i class="fas fa-map fa-3x text-muted mb-3"></i>
                    <p class="text-muted">Live map tracking</p>
                    <div class="mt-3">
                        <div class="loading-spinner"></div>
                        <p class="small text-muted mt-2">Loading map...</p>
                    </div>
                </div>
            `;
            
            // Simulate map loading
            setTimeout(() => {
                mapContainer.innerHTML = `
                    <div class="map-placeholder">
                        <i class="fas fa-map-marked-alt fa-3x text-primary mb-3"></i>
                        <p class="text-muted">Delivery partner is on the way!</p>
                        <p class="small text-muted">Distance: 2.3 km away</p>
                        <p class="small text-muted">ETA: 15 minutes</p>
                    </div>
                `;
            }, 2000);
        }
    }

    // Cleanup
    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    }
}

// Initialize order tracker
let orderTracker;

document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on tracking page
    if (window.location.pathname.includes('order-tracking')) {
        orderTracker = new OrderTracker();
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (orderTracker) {
        orderTracker.destroy();
    }
});
