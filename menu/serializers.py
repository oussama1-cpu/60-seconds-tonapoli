from rest_framework import serializers
from .models import (
    Category, MenuItem, Ingredient, MenuItemIngredient,
    Customization, Review, RestaurantInfo, Branch
)


class CategorySerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'image', 'order', 
            'is_active', 'item_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_item_count(self, obj):
        return obj.items.filter(is_available=True).count()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'description', 'is_allergen']


class MenuItemIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
        write_only=True
    )

    class Meta:
        model = MenuItemIngredient
        fields = ['id', 'ingredient', 'ingredient_id', 'quantity', 'is_optional']


class CustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customization
        fields = [
            'id', 'name', 'customization_type', 'price_modifier', 'is_active'
        ]


class BranchSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = [
            'id', 'name', 'address', 'city', 'phone', 'email',
            'image', 'opening_hours', 'latitude', 'longitude',
            'is_active', 'review_count', 'average_rating', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()

    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None


class ReviewSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'category', 'category_display', 'menu_item', 'menu_item_name',
            'branch', 'branch_name', 'customer_name', 'rating',
            'comment', 'created_at', 'is_approved'
        ]
        read_only_fields = ['created_at', 'is_approved']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def validate(self, data):
        category = data.get('category', 'other')
        if category == 'product' and not data.get('menu_item'):
            raise serializers.ValidationError("Menu item is required for product reviews")
        if category == 'branch' and not data.get('branch'):
            raise serializers.ValidationError("Branch is required for branch reviews")
        return data


class MenuItemListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'category', 'category_name',
            'price', 'image', 'video', 'video_thumbnail', 'spice_level', 
            'is_vegetarian', 'is_vegan', 'is_gluten_free', 'contains_nuts', 
            'is_available', 'is_featured', 'preparation_time', 'calories', 
            'average_rating'
        ]

    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None


class MenuItemDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with all related data"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    ingredients = MenuItemIngredientSerializer(many=True, read_only=True)
    customizations = CustomizationSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'category', 'category_id',
            'price', 'image', 'video', 'video_thumbnail', 'spice_level', 
            'is_vegetarian', 'is_vegan', 'is_gluten_free', 'contains_nuts', 
            'is_available', 'is_featured', 'preparation_time', 'calories', 
            'order', 'ingredients', 'customizations', 'reviews', 
            'average_rating', 'review_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_reviews(self, obj):
        approved_reviews = obj.reviews.filter(is_approved=True)[:5]
        return ReviewSerializer(approved_reviews, many=True).data

    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None

    def get_review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()


class RestaurantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantInfo
        fields = [
            'id', 'name', 'description', 'logo', 'phone', 'email',
            'address', 'opening_hours', 'facebook_url', 'instagram_url',
            'twitter_url', 'currency_symbol', 'tax_rate', 'updated_at'
        ]
        read_only_fields = ['updated_at']
