from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Menu category (e.g., Appetizers, Main Courses, Desserts, Drinks)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Individual menu item"""
    SPICE_LEVELS = [
        ('none', 'Not Spicy'),
        ('mild', 'Mild'),
        ('medium', 'Medium'),
        ('hot', 'Hot'),
        ('extra_hot', 'Extra Hot'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    
    # Media fields for enhanced visualization
    video = models.FileField(upload_to='menu_videos/', blank=True, null=True, help_text="Video of the dish being prepared or presented")
    model_3d = models.FileField(upload_to='menu_3d/', blank=True, null=True, help_text="3D model file (.glb, .gltf, .obj)")
    video_thumbnail = models.ImageField(upload_to='menu_thumbnails/', blank=True, null=True, help_text="Thumbnail for video")
    
    # Additional details
    spice_level = models.CharField(max_length=20, choices=SPICE_LEVELS, default='none')
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    contains_nuts = models.BooleanField(default=False)
    
    # Availability
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show as featured item")
    
    # Metadata
    preparation_time = models.IntegerField(help_text="Preparation time in minutes", null=True, blank=True)
    calories = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(default=0, help_text="Display order within category")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'order', 'name']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return f"{self.name} - {self.category.name}"


class Ingredient(models.Model):
    """Ingredients for menu items"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_allergen = models.BooleanField(default=False, help_text="Mark if this is a common allergen")
    
    # Enhanced fields for detailed ingredient information
    origin = models.CharField(max_length=200, blank=True, help_text="Origin/source of the ingredient")
    nutritional_info = models.TextField(blank=True, help_text="Nutritional information per 100g")
    supplier = models.CharField(max_length=200, blank=True, help_text="Supplier name")
    seasonal = models.BooleanField(default=False, help_text="Is this ingredient seasonal?")
    organic = models.BooleanField(default=False, help_text="Is this ingredient organic?")
    image = models.ImageField(upload_to='ingredients/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MenuItemIngredient(models.Model):
    """Link between menu items and ingredients with quantity"""
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50, blank=True, help_text="e.g., '100g', '2 pieces'")
    is_optional = models.BooleanField(default=False)

    class Meta:
        unique_together = ['menu_item', 'ingredient']
        verbose_name = "Menu Item Ingredient"
        verbose_name_plural = "Menu Item Ingredients"

    def __str__(self):
        return f"{self.ingredient.name} in {self.menu_item.name}"


class Customization(models.Model):
    """Customization options for menu items (e.g., size, extras)"""
    CUSTOMIZATION_TYPES = [
        ('size', 'Size'),
        ('extra', 'Extra'),
        ('side', 'Side Dish'),
        ('sauce', 'Sauce'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    customization_type = models.CharField(max_length=20, choices=CUSTOMIZATION_TYPES)
    price_modifier = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text="Additional price (can be negative for discounts)"
    )
    menu_items = models.ManyToManyField(MenuItem, related_name='customizations', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['customization_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_customization_type_display()})"


class Review(models.Model):
    """Customer reviews with categories: branch, service, product, other"""
    REVIEW_CATEGORIES = [
        ('branch', 'Branch/Location'),
        ('service', 'Service/Staff'),
        ('product', 'Product/Food'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=20, choices=REVIEW_CATEGORIES, default='other')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True, help_text="Only for product reviews")
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='reviews', null=True, blank=True, help_text="Only for branch reviews")
    customer_name = models.CharField(max_length=100)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, help_text="Approve review to display publicly")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.category == 'product' and self.menu_item:
            return f"{self.customer_name} - {self.menu_item.name} ({self.rating}★)"
        elif self.category == 'branch' and self.branch:
            return f"{self.customer_name} - {self.branch.name} ({self.rating}★)"
        return f"{self.customer_name} - {self.get_category_display()} ({self.rating}★)"


class Branch(models.Model):
    """Restaurant branches/locations"""
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='branches/', blank=True, null=True)
    
    # Opening hours
    opening_hours = models.TextField(blank=True, help_text="Opening hours for this branch")
    
    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Branches"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.city}"


class RestaurantInfo(models.Model):
    """Restaurant information (singleton model)"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='restaurant/', blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    
    # Opening hours
    opening_hours = models.TextField(help_text="Enter opening hours")
    
    # Social media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    # Settings
    currency_symbol = models.CharField(max_length=5, default='€')
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Tax rate in percentage")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Restaurant Information"
        verbose_name_plural = "Restaurant Information"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and RestaurantInfo.objects.exists():
            raise ValueError("Only one RestaurantInfo instance is allowed")
        return super().save(*args, **kwargs)
