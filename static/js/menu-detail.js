const quantityInput = document.getElementById('quantity');
const decreaseBtn = document.getElementById('decrease-qty');
const increaseBtn = document.getElementById('increase-qty');
const addToCartBtn = document.getElementById('add-to-cart');
const addToFavoritesBtn = document.getElementById('add-to-favorites');

if (quantityInput && decreaseBtn && increaseBtn) {
    decreaseBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const currentValue = parseInt(quantityInput.value, 10);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    });

    increaseBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const currentValue = parseInt(quantityInput.value, 10);
        if (currentValue < 10) {
            quantityInput.value = currentValue + 1;
        }
    });
}

if (addToCartBtn && quantityInput) {
    addToCartBtn.addEventListener('click', function() {
        const quantity = parseInt(quantityInput.value, 10);
        const customizations = [];

        document.querySelectorAll('input[type="radio"]:checked, input[type="checkbox"]:checked').forEach(input => {
            customizations.push(parseInt(input.value, 10));
        });

        console.log('Adding to cart:', {
            itemId: addToCartBtn.dataset.itemId,
            quantity: quantity,
            customizations: customizations
        });

        alert('Item added to cart!');
    });
}

if (addToFavoritesBtn) {
    addToFavoritesBtn.addEventListener('click', function() {
        console.log('Adding to favorites:', addToFavoritesBtn.dataset.itemId);

        const icon = this.querySelector('i');
        icon.classList.remove('far');
        icon.classList.add('fas', 'text-danger');
        this.textContent = ' Added to Favorites';
        this.insertBefore(icon, this.firstChild);

        setTimeout(() => {
            icon.classList.remove('fas', 'text-danger');
            icon.classList.add('far');
            this.textContent = 'Add to Favorites';
            this.insertBefore(icon, this.firstChild);
        }, 2000);
    });
}
