// Enhanced Menu Detail JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Rating System
    const ratingStars = document.querySelectorAll('.rating-star');
    const ratingValue = document.getElementById('rating-value');
    
    if (ratingStars.length > 0) {
        ratingStars.forEach(star => {
            star.addEventListener('click', function() {
                const rating = parseInt(this.dataset.rating);
                ratingValue.value = rating;
                updateRatingDisplay(rating);
            });
            
            star.addEventListener('mouseenter', function() {
                const rating = parseInt(this.dataset.rating);
                updateRatingDisplay(rating);
            });
        });
        
        document.querySelector('.rating-input').addEventListener('mouseleave', function() {
            updateRatingDisplay(parseInt(ratingValue.value));
        });
        
        function updateRatingDisplay(rating) {
            ratingStars.forEach((star, index) => {
                if (index < rating) {
                    star.classList.remove('far');
                    star.classList.add('fas', 'active');
                } else {
                    star.classList.remove('fas', 'active');
                    star.classList.add('far');
                }
            });
        }
        
        // Initialize display
        updateRatingDisplay(parseInt(ratingValue.value));
    }
    
    // Review Form Submission
    const reviewForm = document.getElementById('review-form');
    const submitReviewBtn = document.getElementById('submit-review');
    
    if (submitReviewBtn) {
        submitReviewBtn.addEventListener('click', function() {
            if (reviewForm.checkValidity()) {
                const formData = new FormData(reviewForm);
                submitReview(formData);
            } else {
                reviewForm.reportValidity();
            }
        });
    }
    
    function submitReview(formData) {
        // Show loading state
        submitReviewBtn.disabled = true;
        submitReviewBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Submitting...';
        
        // Submit review to API
        fetch('/submit-review/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                menu_item_id: formData.get('menu_item_id'),
                customer_name: formData.get('customer-name'),
                rating: formData.get('rating'),
                comment: formData.get('review-comment')
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('reviewModal'));
                modal.hide();
                
                // Reset form
                reviewForm.reset();
                updateRatingDisplay(5);
                
                // Show success message
                showNotification(data.message || 'Review submitted successfully!', 'success');
                
                // Optionally refresh reviews list
                setTimeout(() => {
                    location.reload();
                }, 2000);
            } else {
                showNotification(data.error || 'Failed to submit review', 'danger');
            }
        })
        .catch(error => {
            console.error('Error submitting review:', error);
            showNotification('Failed to submit review. Please try again.', 'danger');
        })
        .finally(() => {
            // Reset button
            submitReviewBtn.disabled = false;
            submitReviewBtn.innerHTML = 'Submit Review';
        });
    }
    
    // 3D Model Loader
    const load3DBtn = document.getElementById('load-3d-model');
    const model3dViewer = document.getElementById('model3d-viewer');
    
    if (load3DBtn && model3dViewer) {
        load3DBtn.addEventListener('click', function() {
            load3DModel();
        });
    }
    
    function load3DModel() {
        const btn = document.getElementById('load-3d-model');
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
        
        // Simulate 3D model loading (replace with actual 3D library like Three.js)
        setTimeout(() => {
            model3dViewer.innerHTML = `
                <div class="text-center text-white p-4">
                    <i class="fas fa-cube fa-4x mb-3"></i>
                    <h5>3D Model Loaded</h5>
                    <p>Interactive 3D viewer would be implemented here</p>
                    <div class="mt-3">
                        <button class="btn btn-light btn-sm me-2" onclick="rotateModel('left')">
                            <i class="fas fa-undo"></i> Rotate Left
                        </button>
                        <button class="btn btn-light btn-sm me-2" onclick="rotateModel('right')">
                            <i class="fas fa-redo"></i> Rotate Right
                        </button>
                        <button class="btn btn-light btn-sm" onclick="resetModel()">
                            <i class="fas fa-sync"></i> Reset
                        </button>
                    </div>
                </div>
            `;
        }, 2000);
    }
    
    // Video Player Enhancement
    const videos = document.querySelectorAll('video');
    videos.forEach(video => {
        // Add custom event listeners for video analytics
        video.addEventListener('play', function() {
            console.log('Video started playing');
        });
        
        video.addEventListener('ended', function() {
            console.log('Video finished playing');
        });
    });
    
    // Ingredient Detail Modal
    const ingredientCards = document.querySelectorAll('.ingredient-card');
    ingredientCards.forEach(card => {
        card.addEventListener('click', function() {
            // Could open a modal with detailed ingredient information
            console.log('Ingredient card clicked');
        });
    });
    
    // Notification System
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
    
    // Tab Analytics
    const mediaTabs = document.querySelectorAll('#mediaTabs button');
    mediaTabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function(e) {
            const target = e.target.getAttribute('data-bs-target');
            console.log('Media tab switched to:', target);
        });
    });
});

// Global functions for 3D model controls
function rotateModel(direction) {
    console.log('Rotating model:', direction);
    // Implement actual 3D model rotation
}

function resetModel() {
    console.log('Resetting model');
    // Implement actual 3D model reset
}

// Helper function to get CSRF token
function getCookie(name) {
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
}
