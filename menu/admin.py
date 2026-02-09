from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from .models import (
    Category, MenuItem, Ingredient, MenuItemIngredient,
    Customization, Review, RestaurantInfo, Branch
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'item_count', 'image_preview', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Number of Items'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'


class MenuItemIngredientInline(admin.TabularInline):
    model = MenuItemIngredient
    extra = 1
    autocomplete_fields = ['ingredient']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'price', 'is_available', 'is_featured', 
        'image_preview', 'dietary_info', 'rating_display', 'created_at'
    ]
    list_editable = ['is_available', 'is_featured', 'price']
    list_filter = [
        'category', 'is_available', 'is_featured', 'is_vegetarian', 
        'is_vegan', 'is_gluten_free', 'spice_level', 'created_at'
    ]
    search_fields = ['name', 'description']
    autocomplete_fields = ['category']
    filter_horizontal = []
    inlines = [MenuItemIngredientInline]
    readonly_fields = ['rating_display', 'review_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'price', 'image')
        }),
        ('Media Files', {
            'fields': ('video', 'video_thumbnail', 'model_3d'),
            'classes': ('collapse',)
        }),
        ('Dietary Information', {
            'fields': (
                'spice_level', 'is_vegetarian', 'is_vegan', 
                'is_gluten_free', 'contains_nuts'
            )
        }),
        ('Availability & Display', {
            'fields': ('is_available', 'is_featured', 'order')
        }),
        ('Additional Details', {
            'fields': ('preparation_time', 'calories'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

    def dietary_info(self, obj):
        badges = []
        if obj.is_vegetarian:
            badges.append('<span style="background: #4CAF50; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px;">VEG</span>')
        if obj.is_vegan:
            badges.append('<span style="background: #8BC34A; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px;">VEGAN</span>')
        if obj.is_gluten_free:
            badges.append('<span style="background: #FF9800; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px;">GF</span>')
        if obj.contains_nuts:
            badges.append('<span style="background: #F44336; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px;">NUTS</span>')
        return format_html(' '.join(badges)) if badges else '-'
    dietary_info.short_description = 'Dietary'
    
    def rating_display(self, obj):
        approved_reviews = obj.reviews.filter(is_approved=True)
        if approved_reviews.exists():
            avg_rating = approved_reviews.aggregate(models.Avg('rating'))['rating__avg']
            count = approved_reviews.count()
            stars = '★' * int(round(avg_rating)) + '☆' * (5 - int(round(avg_rating)))
            return format_html('<span style="color: #ffc107;">{} ({})</span>', stars, count)
        return "No reviews"
    rating_display.short_description = 'Rating'
    
    def review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()
    review_count.short_description = 'Reviews'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'origin', 'organic', 'seasonal', 'is_allergen', 'image_preview', 'created_at']
    list_filter = ['is_allergen', 'organic', 'seasonal', 'created_at']
    search_fields = ['name', 'description', 'origin', 'supplier']
    list_editable = ['is_allergen', 'organic', 'seasonal']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image')
        }),
        ('Origin & Quality', {
            'fields': ('origin', 'supplier', 'organic', 'seasonal')
        }),
        ('Allergy Information', {
            'fields': ('is_allergen',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: cover; border-radius: 3px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'


@admin.register(Customization)
class CustomizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'customization_type', 'price_modifier', 'is_active', 'item_count']
    list_editable = ['is_active']
    list_filter = ['customization_type', 'is_active', 'created_at']
    search_fields = ['name']
    filter_horizontal = ['menu_items']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'customization_type', 'price_modifier')
        }),
        ('Menu Items', {
            'fields': ('menu_items',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )

    def item_count(self, obj):
        return obj.menu_items.count()
    item_count.short_description = 'Applies to Items'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'category', 'get_related_item', 'rating_stars', 'is_approved', 'created_at', 'comment_preview']
    list_filter = ['category', 'rating', 'is_approved', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['customer_name', 'comment', 'menu_item__name', 'branch__name']
    readonly_fields = ['created_at']
    actions = ['approve_reviews', 'reject_reviews']
    
    fieldsets = (
        ('Review Type', {
            'fields': ('category',)
        }),
        ('Related Item (based on category)', {
            'fields': ('menu_item', 'branch'),
            'description': 'Select menu item for Product reviews, branch for Branch reviews'
        }),
        ('Review Information', {
            'fields': ('customer_name', 'rating', 'comment')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'created_at')
        }),
    )
    
    def get_related_item(self, obj):
        if obj.category == 'product' and obj.menu_item:
            return obj.menu_item.name
        elif obj.category == 'branch' and obj.branch:
            return obj.branch.name
        return '-'
    get_related_item.short_description = 'Related To'
    
    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: #ffc107;">{}</span>', stars)
    rating_stars.short_description = 'Rating'
    
    def comment_preview(self, obj):
        if len(obj.comment) > 50:
            return obj.comment[:50] + '...'
        return obj.comment
    comment_preview.short_description = 'Comment'
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} reviews approved successfully.")
    approve_reviews.short_description = "Approve selected reviews"
    
    def reject_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} reviews rejected successfully.")
    reject_reviews.short_description = "Reject selected reviews"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('menu_item', 'menu_item__category', 'branch')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'phone', 'is_active', 'review_count', 'image_preview', 'created_at']
    list_filter = ['city', 'is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['name', 'address', 'city']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'city', 'address', 'image')
        }),
        ('Contact', {
            'fields': ('phone', 'email')
        }),
        ('Hours & Location', {
            'fields': ('opening_hours', 'latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'
    
    def review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()
    review_count.short_description = 'Reviews'


@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'logo')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address', 'opening_hours')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('currency_symbol', 'tax_rate')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not RestaurantInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False
