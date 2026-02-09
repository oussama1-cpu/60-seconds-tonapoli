from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from .models import Category, MenuItem, Ingredient, Review, RestaurantInfo


class CategoryModelTest(TestCase):
    """Test Category model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description",
            order=1,
            is_active=True
        )
    
    def test_category_creation(self):
        """Test category is created correctly"""
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.order, 1)
        self.assertTrue(self.category.is_active)
    
    def test_category_str(self):
        """Test category string representation"""
        self.assertEqual(str(self.category), "Test Category")


class MenuItemModelTest(TestCase):
    """Test MenuItem model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Pizzas",
            order=1
        )
        self.menu_item = MenuItem.objects.create(
            name="Margherita",
            description="Classic pizza",
            category=self.category,
            price=Decimal('12.99'),
            is_vegetarian=True,
            is_available=True
        )
    
    def test_menu_item_creation(self):
        """Test menu item is created correctly"""
        self.assertEqual(self.menu_item.name, "Margherita")
        self.assertEqual(self.menu_item.price, Decimal('12.99'))
        self.assertTrue(self.menu_item.is_vegetarian)
        self.assertTrue(self.menu_item.is_available)
    
    def test_menu_item_str(self):
        """Test menu item string representation"""
        self.assertEqual(str(self.menu_item), "Margherita - Pizzas")


class CategoryAPITest(APITestCase):
    """Test Category API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Appetizers",
            description="Starters",
            order=1,
            is_active=True
        )
    
    def test_get_categories(self):
        """Test retrieving categories list"""
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_category_detail(self):
        """Test retrieving a single category"""
        response = self.client.get(f'/api/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Appetizers")


class MenuItemAPITest(APITestCase):
    """Test MenuItem API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Main Courses",
            order=1
        )
        self.menu_item = MenuItem.objects.create(
            name="Pasta Carbonara",
            description="Creamy pasta",
            category=self.category,
            price=Decimal('15.99'),
            is_available=True,
            is_featured=True
        )
    
    def test_get_menu_items(self):
        """Test retrieving menu items list"""
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_menu_item_detail(self):
        """Test retrieving a single menu item"""
        response = self.client.get(f'/api/menu-items/{self.menu_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Pasta Carbonara")
    
    def test_get_featured_items(self):
        """Test retrieving featured items"""
        response = self.client.get('/api/menu-items/featured/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_search_menu_items(self):
        """Test searching menu items"""
        response = self.client.get('/api/menu-items/search/?q=pasta')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_filter_by_category(self):
        """Test filtering items by category"""
        response = self.client.get(f'/api/menu-items/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class ReviewAPITest(APITestCase):
    """Test Review API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Desserts", order=1)
        self.menu_item = MenuItem.objects.create(
            name="Tiramisu",
            description="Italian dessert",
            category=self.category,
            price=Decimal('7.99'),
            is_available=True
        )
    
    def test_create_review(self):
        """Test creating a review"""
        data = {
            'menu_item': self.menu_item.id,
            'customer_name': 'John Doe',
            'rating': 5,
            'comment': 'Excellent!'
        }
        response = self.client.post('/api/reviews/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_review_requires_approval(self):
        """Test that new reviews are not approved by default"""
        data = {
            'menu_item': self.menu_item.id,
            'customer_name': 'Jane Doe',
            'rating': 4,
            'comment': 'Very good'
        }
        self.client.post('/api/reviews/', data)
        review = Review.objects.first()
        self.assertFalse(review.is_approved)


class RestaurantInfoAPITest(APITestCase):
    """Test RestaurantInfo API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.restaurant_info = RestaurantInfo.objects.create(
            name="Test Restaurant",
            description="A test restaurant",
            phone="+1234567890",
            email="test@restaurant.com",
            address="123 Test St",
            opening_hours="Mon-Sun: 10:00-22:00"
        )
    
    def test_get_restaurant_info(self):
        """Test retrieving restaurant information"""
        response = self.client.get('/api/restaurant-info/current/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Restaurant")
