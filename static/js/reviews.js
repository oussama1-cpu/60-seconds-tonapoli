/**
 * Reviews Component
 * Handles review display, submission, and rating interactions
 */

class ReviewsManager {
    constructor() {
        this.apiEndpoint = '/api/reviews/';
        this.submitEndpoint = '/submit-review/';
        this.init();
    }

    init() {
        this.initRatingInputs();
        this.initReviewForms();
        this.loadReviews();
    }

    // Initialize star rating inputs
    initRatingInputs() {
        document.querySelectorAll('.rating-input').forEach(container => {
            const stars = container.querySelectorAll('.star-btn');
            const input = container.querySelector('input[type="hidden"]');

            stars.forEach((star, index) => {
                star.addEventListener('click', () => {
                    const rating = index + 1;
                    if (input) input.value = rating;
                    this.updateStars(stars, rating);
                });

                star.addEventListener('mouseenter', () => {
                    this.updateStars(stars, index + 1);
                });
            });

            container.addEventListener('mouseleave', () => {
                const currentRating = input ? parseInt(input.value) || 0 : 0;
                this.updateStars(stars, currentRating);
            });
        });
    }

    updateStars(stars, rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.add('active');
                star.innerHTML = '<i class="fas fa-star"></i>';
            } else {
                star.classList.remove('active');
                star.innerHTML = '<i class="far fa-star"></i>';
            }
        });
    }

    // Initialize review submission forms
    initReviewForms() {
        document.querySelectorAll('.review-form').forEach(form => {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.submitReview(form);
            });
        });
    }

    async submitReview(form) {
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;

        try {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Submitting...';

            const response = await fetch(this.submitEndpoint, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            const data = await response.json();

            if (data.success) {
                this.showToast('Thank you! Your review has been submitted for approval.', 'success');
                form.reset();
                this.updateStars(form.querySelectorAll('.star-btn'), 0);
            } else {
                this.showToast(data.error || 'Failed to submit review', 'error');
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            this.showToast('An error occurred. Please try again.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    }

    // Load reviews for display
    async loadReviews(menuItemId = null) {
        const container = document.getElementById('reviews-container');
        if (!container) return;

        try {
            let url = this.apiEndpoint;
            if (menuItemId) {
                url += `?menu_item=${menuItemId}`;
            }

            const response = await fetch(url);
            const data = await response.json();

            if (data.results && data.results.length > 0) {
                this.renderReviews(container, data.results);
                this.updateReviewStats(data.results);
            } else {
                container.innerHTML = this.getEmptyState();
            }
        } catch (error) {
            console.error('Error loading reviews:', error);
        }
    }

    renderReviews(container, reviews) {
        const html = reviews.map(review => this.createReviewCard(review)).join('');
        container.innerHTML = `<div class="row g-4">${html}</div>`;
    }

    createReviewCard(review) {
        const initials = review.customer_name.split(' ').map(n => n[0]).join('').toUpperCase();
        const stars = this.createStarsHTML(review.rating);
        const date = new Date(review.created_at).toLocaleDateString('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });

        return `
            <div class="col-md-6 col-lg-4">
                <div class="review-card">
                    <div class="review-header">
                        <div class="review-avatar">${initials}</div>
                        <div class="review-info">
                            <div class="review-author">${this.escapeHtml(review.customer_name)}</div>
                            <div class="review-date">${date}</div>
                        </div>
                    </div>
                    <div class="review-rating">${stars}</div>
                    <p class="review-content">${this.escapeHtml(review.comment)}</p>
                    ${review.menu_item_name ? `
                        <div class="review-menu-item">
                            <i class="fas fa-utensils"></i>
                            <span>${this.escapeHtml(review.menu_item_name)}</span>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    createStarsHTML(rating) {
        let html = '';
        for (let i = 1; i <= 5; i++) {
            if (i <= rating) {
                html += '<i class="fas fa-star star filled"></i>';
            } else {
                html += '<i class="far fa-star star"></i>';
            }
        }
        return html;
    }

    updateReviewStats(reviews) {
        const statsContainer = document.getElementById('review-stats');
        if (!statsContainer || reviews.length === 0) return;

        const totalReviews = reviews.length;
        const avgRating = (reviews.reduce((sum, r) => sum + r.rating, 0) / totalReviews).toFixed(1);
        
        // Count ratings
        const ratingCounts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0};
        reviews.forEach(r => ratingCounts[r.rating]++);

        statsContainer.innerHTML = `
            <div class="review-stats-average">
                <div class="review-stats-number">${avgRating}</div>
                <div class="review-stats-stars">${this.createStarsHTML(Math.round(avgRating))}</div>
                <div class="review-stats-count">${totalReviews} avis</div>
            </div>
            <div class="review-stats-bars">
                ${[5, 4, 3, 2, 1].map(rating => `
                    <div class="review-bar">
                        <span class="review-bar-label">${rating} étoiles</span>
                        <div class="review-bar-track">
                            <div class="review-bar-fill" style="width: ${(ratingCounts[rating] / totalReviews) * 100}%"></div>
                        </div>
                        <span class="review-bar-count">${ratingCounts[rating]}</span>
                    </div>
                `).join('')}
            </div>
        `;
    }

    getEmptyState() {
        return `
            <div class="text-center py-5">
                <i class="fas fa-comments fa-3x text-muted mb-3"></i>
                <h4 class="text-white">No reviews yet</h4>
                <p class="text-muted">Be the first to share your experience!</p>
            </div>
        `;
    }

    getCSRFToken() {
        const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
        return cookie ? cookie.split('=')[1] : '';
    }

    showToast(message, type = 'info') {
        if (typeof NapoliApp !== 'undefined' && NapoliApp.toast) {
            NapoliApp.toast.show(message, type);
        } else {
            alert(message);
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.reviewsManager = new ReviewsManager();
});
