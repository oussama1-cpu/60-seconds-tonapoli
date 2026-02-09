// Enhanced Menu Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    let allMenuItems = [];
    let filteredItems = [];
    let currentFilters = {
        search: '',
        vegetarian: false,
        vegan: false,
        glutenfree: false,
        sort: 'name'
    };
    
    // Initialize menu items
    initializeMenuItems();
    updateStats();
    
    // Event Listeners
    document.getElementById('search-input').addEventListener('input', handleSearch);
    document.getElementById('sort-select').addEventListener('change', handleSort);
    document.getElementById('filter-vegetarian').addEventListener('change', handleFilter);
    document.getElementById('filter-vegan').addEventListener('change', handleFilter);
    document.getElementById('filter-glutenfree').addEventListener('change', handleFilter);
    document.getElementById('clear-filters').addEventListener('click', clearAllFilters);
    
    // Quick view buttons
    document.querySelectorAll('.quick-view-btn').forEach(btn => {
        btn.addEventListener('click', handleQuickView);
    });
    
    // Wishlist buttons
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
        btn.addEventListener('click', handleWishlist);
    });
    
    // Add to cart buttons
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', handleAddToCart);
    });
    
    // Category navigation
    document.querySelectorAll('.category-nav-link').forEach(link => {
        link.addEventListener('click', handleCategoryNav);
    });
    
    function initializeMenuItems() {
        allMenuItems = Array.from(document.querySelectorAll('.menu-item-wrapper'));
        filteredItems = [...allMenuItems];
    }
    
    function handleSearch(e) {
        currentFilters.search = e.target.value.toLowerCase();
        applyFilters();
    }
    
    function handleSort(e) {
        currentFilters.sort = e.target.value;
        applyFilters();
    }
    
    function handleFilter(e) {
        const filterType = e.target.id.replace('filter-', '');
        currentFilters[filterType] = e.target.checked;
        applyFilters();
        updateFilterTags();
    }
    
    function applyFilters() {
        showLoading();
        
        setTimeout(() => {
            filteredItems = allMenuItems.filter(item => {
                // Search filter
                if (currentFilters.search) {
                    const name = item.dataset.itemName || '';
                    const category = item.dataset.itemCategory || '';
                    if (!name.includes(currentFilters.search) && !category.includes(currentFilters.search)) {
                        return false;
                    }
                }
                
                // Dietary filters
                if (currentFilters.vegetarian && item.dataset.vegetarian !== 'true') return false;
                if (currentFilters.vegan && item.dataset.vegan !== 'true') return false;
                if (currentFilters.glutenfree && item.dataset.glutenfree !== 'true') return false;
                
                return true;
            });
            
            // Apply sorting
            sortItems();
            
            // Update display
            updateDisplay();
            hideLoading();
            updateStats();
        }, 300);
    }
    
    function sortItems() {
        const sortType = currentFilters.sort;
        const container = document.getElementById('menu-items-container');
        const sections = Array.from(container.querySelectorAll('.category-section'));
        
        sections.forEach(section => {
            const items = Array.from(section.querySelectorAll('.menu-item-wrapper'));
            const filteredSectionItems = items.filter(item => filteredItems.includes(item));
            
            filteredSectionItems.sort((a, b) => {
                switch (sortType) {
                    case 'name':
                        return (a.dataset.itemName || '').localeCompare(b.dataset.itemName || '');
                    case 'price-low':
                        return parseFloat(a.dataset.itemPrice) - parseFloat(b.dataset.itemPrice);
                    case 'price-high':
                        return parseFloat(b.dataset.itemPrice) - parseFloat(a.dataset.itemPrice);
                    case 'rating':
                        return parseFloat(b.dataset.rating) - parseFloat(a.dataset.rating);
                    case 'popular':
                        return (b.dataset.featured === 'true' ? 1 : 0) - (a.dataset.featured === 'true' ? 1 : 0);
                    default:
                        return 0;
                }
            });
            
            // Reorder items in the section
            const grid = section.querySelector('.menu-items-grid');
            filteredSectionItems.forEach(item => grid.appendChild(item));
            
            // Hide sections with no items
            section.style.display = filteredSectionItems.length > 0 ? 'block' : 'none';
        });
    }
    
    function updateDisplay() {
        // Hide all items first
        allMenuItems.forEach(item => {
            item.style.display = 'none';
            item.classList.remove('filtered');
        });
        
        // Show filtered items
        filteredItems.forEach(item => {
            item.style.display = 'block';
            item.classList.add('filtered', 'fade-in');
        });
        
        // Show/hide no results message
        const noResults = document.getElementById('no-results');
        noResults.style.display = filteredItems.length === 0 ? 'block' : 'none';
    }
    
    function updateStats() {
        const totalItems = allMenuItems.length;
        const filteredCount = filteredItems.length;
        
        document.getElementById('total-items').textContent = totalItems;
        document.getElementById('filtered-items').textContent = filteredCount;
        
        // Update category counts
        document.querySelectorAll('.category-section').forEach(section => {
            const categoryId = section.dataset.categoryId;
            const visibleItems = section.querySelectorAll('.menu-item-wrapper.filtered');
            const countBadge = section.querySelector('.category-count');
            if (countBadge) {
                countBadge.textContent = `${visibleItems.length} items`;
            }
        });
    }
    
    function updateFilterTags() {
        const tagsContainer = document.getElementById('filter-tags');
        const tags = [];
        
        if (currentFilters.search) {
            tags.push(`<span class="filter-pill">Search: "${currentFilters.search}"</span>`);
        }
        if (currentFilters.vegetarian) {
            tags.push(`<span class="filter-pill">Vegetarian <span class="close" data-filter="vegetarian">×</span></span>`);
        }
        if (currentFilters.vegan) {
            tags.push(`<span class="filter-pill">Vegan <span class="close" data-filter="vegan">×</span></span>`);
        }
        if (currentFilters.glutenfree) {
            tags.push(`<span class="filter-pill">Gluten-Free <span class="close" data-filter="glutenfree">×</span></span>`);
        }
        
        tagsContainer.innerHTML = tags.join('');
        
        // Add event listeners to close buttons
        tagsContainer.querySelectorAll('.close').forEach(closeBtn => {
            closeBtn.addEventListener('click', function() {
                const filter = this.dataset.filter;
                document.getElementById(`filter-${filter}`).checked = false;
                currentFilters[filter] = false;
                applyFilters();
                updateFilterTags();
            });
        });
    }
    
    function clearAllFilters() {
        // Reset all filters
        currentFilters = {
            search: '',
            vegetarian: false,
            vegan: false,
            glutenfree: false,
            sort: 'name'
        };
        
        // Reset UI
        document.getElementById('search-input').value = '';
        document.getElementById('sort-select').value = 'name';
        document.getElementById('filter-vegetarian').checked = false;
        document.getElementById('filter-vegan').checked = false;
        document.getElementById('filter-glutenfree').checked = false;
        
        applyFilters();
        updateFilterTags();
    }
    
    function handleQuickView(e) {
        const itemId = e.currentTarget.dataset.itemId;
        const itemElement = document.querySelector(`.menu-item-wrapper[data-item-id="${itemId}"]`);
        
        if (!itemElement) return;
        
        // Extract item data
        const itemName = itemElement.querySelector('.card-title').textContent;
        const itemPrice = itemElement.querySelector('.text-primary').textContent;
        const itemImage = itemElement.querySelector('.menu-item-img')?.src || '';
        const itemDescription = itemElement.querySelector('.card-text')?.textContent || '';
        
        // Populate modal
        document.getElementById('quickViewTitle').textContent = itemName;
        document.getElementById('quickViewBody').innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    ${itemImage ? `<img src="${itemImage}" class="img-fluid rounded" alt="${itemName}">` : 
                      '<div class="bg-light d-flex align-items-center justify-content-center" style="height: 250px;"><i class="fas fa-utensils fa-3x text-muted"></i></div>'}
                </div>
                <div class="col-md-6">
                    <h4>${itemName}</h4>
                    <div class="h3 text-primary mb-3">${itemPrice}</div>
                    ${itemDescription ? `<p>${itemDescription}</p>` : ''}
                    
                    <div class="mt-4">
                        <div class="mb-3">
                            <label class="form-label">Quantity</label>
                            <div class="input-group" style="width: 150px;">
                                <button class="btn btn-outline-secondary" type="button" onclick="this.nextElementSibling.value = Math.max(1, parseInt(this.nextElementSibling.value) - 1)">-</button>
                                <input type="number" class="form-control text-center" value="1" min="1" max="10">
                                <button class="btn btn-outline-secondary" type="button" onclick="this.previousElementSibling.value = Math.min(10, parseInt(this.previousElementSibling.value) + 1)">+</button>
                            </div>
                        </div>
                        
                        <div class="d-flex gap-2">
                            <button class="btn btn-primary flex-fill" onclick="addToCartFromQuickView('${itemId}')">
                                <i class="fas fa-shopping-cart me-2"></i>Add to Cart
                            </button>
                            <button class="btn btn-outline-danger" onclick="toggleWishlistFromQuickView('${itemId}')">
                                <i class="far fa-heart"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Set add to cart button data
        document.getElementById('quickViewAddToCart').dataset.itemId = itemId;
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('quickViewModal'));
        modal.show();
    }
    
    function handleWishlist(e) {
        const btn = e.currentTarget;
        const itemId = btn.dataset.itemId;
        
        btn.classList.toggle('active');
        const isActive = btn.classList.contains('active');
        
        if (isActive) {
            btn.innerHTML = '<i class="fas fa-heart"></i>';
            showNotification('Added to wishlist!', 'success');
        } else {
            btn.innerHTML = '<i class="far fa-heart"></i>';
            showNotification('Removed from wishlist', 'info');
        }
        
        // Save to localStorage
        const wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');
        if (isActive) {
            wishlist.push(itemId);
        } else {
            const index = wishlist.indexOf(itemId);
            if (index > -1) wishlist.splice(index, 1);
        }
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
    }
    
    function handleAddToCart(e) {
        const btn = e.currentTarget;
        const itemId = btn.dataset.itemId;
        
        // Add loading state
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Adding...';
        
        setTimeout(() => {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-shopping-cart me-1"></i>Add';
            showNotification('Added to cart!', 'success');
            
            // Update cart count (if implemented)
            updateCartCount();
        }, 1000);
    }
    
    function handleCategoryNav(e) {
        e.preventDefault();
        const targetId = e.currentTarget.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
            // Update active state
            document.querySelectorAll('.category-nav-link').forEach(link => {
                link.classList.remove('active');
            });
            e.currentTarget.classList.add('active');
        }
    }
    
    function showLoading() {
        document.getElementById('loading-indicator').style.display = 'block';
        document.getElementById('menu-items-container').style.opacity = '0.5';
    }
    
    function hideLoading() {
        document.getElementById('loading-indicator').style.display = 'none';
        document.getElementById('menu-items-container').style.opacity = '1';
    }
    
    function updateCartCount() {
        // Update cart count if cart functionality is implemented
        const cartCount = document.querySelector('.fa-shopping-cart').nextElementSibling;
        if (cartCount) {
            const currentCount = parseInt(cartCount.textContent) || 0;
            cartCount.textContent = currentCount + 1;
        }
    }
    
    function showNotification(message, type = 'info') {
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
    
    // Load wishlist state on page load
    function loadWishlistState() {
        const wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');
        wishlist.forEach(itemId => {
            const btn = document.querySelector(`.wishlist-btn[data-item-id="${itemId}"]`);
            if (btn) {
                btn.classList.add('active');
                btn.innerHTML = '<i class="fas fa-heart"></i>';
            }
        });
    }
    
    loadWishlistState();
});

// Global functions for quick view modal
function addToCartFromQuickView(itemId) {
    const quantityInput = document.querySelector('#quickViewBody input[type="number"]');
    const quantity = parseInt(quantityInput.value) || 1;
    
    showNotification(`Added ${quantity} item(s) to cart!`, 'success');
    
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('quickViewModal'));
    modal.hide();
    
    updateCartCount();
}

function toggleWishlistFromQuickView(itemId) {
    const btn = document.querySelector('#quickViewBody .btn-outline-danger');
    const wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');
    
    if (wishlist.includes(itemId)) {
        // Remove from wishlist
        const index = wishlist.indexOf(itemId);
        wishlist.splice(index, 1);
        btn.innerHTML = '<i class="far fa-heart"></i>';
        showNotification('Removed from wishlist', 'info');
    } else {
        // Add to wishlist
        wishlist.push(itemId);
        btn.innerHTML = '<i class="fas fa-heart"></i>';
        showNotification('Added to wishlist!', 'success');
    }
    
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    
    // Update main wishlist button
    const mainBtn = document.querySelector(`.wishlist-btn[data-item-id="${itemId}"]`);
    if (mainBtn) {
        if (wishlist.includes(itemId)) {
            mainBtn.classList.add('active');
            mainBtn.innerHTML = '<i class="fas fa-heart"></i>';
        } else {
            mainBtn.classList.remove('active');
            mainBtn.innerHTML = '<i class="far fa-heart"></i>';
        }
    }
}
