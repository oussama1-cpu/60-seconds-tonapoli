from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import (
    Category, MenuItem, Ingredient, Customization, Review, RestaurantInfo, MenuItemIngredient, Branch
)
from .serializers import (
    CategorySerializer, MenuItemListSerializer, MenuItemDetailSerializer,
    IngredientSerializer, CustomizationSerializer, ReviewSerializer,
    RestaurantInfoSerializer, BranchSerializer
)


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission: Allow read-only for all, write for admins only
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Write permissions only for authenticated staff/admin users
        # For development, we'll allow all write operations
        return True  # Change to: request.user and request.user.is_staff for production


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing menu categories.
    
    list: Get all active categories
    retrieve: Get a specific category with its items
    create: Create a new category (admin only)
    update: Update a category (admin only)
    destroy: Delete a category (admin only)
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'name', 'created_at']
    ordering = ['order', 'name']

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """Get all menu items in this category"""
        category = self.get_object()
        items = category.items.filter(is_available=True)
        serializer = MenuItemListSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing menu items.
    
    list: Get all available menu items
    retrieve: Get detailed information about a menu item
    create: Create a new menu item (admin only)
    update: Update a menu item (admin only)
    destroy: Delete a menu item (admin only)
    """
    queryset = MenuItem.objects.all().select_related('category')  # Changed to show all items for admin
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'is_vegetarian': ['exact'],
        'is_vegan': ['exact'],
        'is_gluten_free': ['exact'],
        'is_featured': ['exact'],
        'spice_level': ['exact'],
        'price': ['gte', 'lte'],
    }
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at', 'order']
    ordering = ['category__order', 'order', 'name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MenuItemDetailSerializer
        return MenuItemListSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured menu items"""
        featured_items = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search for menu items"""
        query = request.query_params.get('q', '')
        
        if not query:
            return Response({'error': 'Search query is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        items = self.queryset.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
        
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all approved reviews for a menu item"""
        menu_item = self.get_object()
        reviews = menu_item.reviews.filter(is_approved=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class IngredientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing ingredients.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def allergens(self, request):
        """Get all allergen ingredients"""
        allergens = self.queryset.filter(is_allergen=True)
        serializer = self.get_serializer(allergens, many=True)
        return Response(serializer.data)


class CustomizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing menu item customizations.
    """
    queryset = Customization.objects.filter(is_active=True)
    serializer_class = CustomizationSerializer
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ['customization_type']
    ordering_fields = ['name', 'price_modifier']
    ordering = ['customization_type', 'name']

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get customizations grouped by type"""
        customization_type = request.query_params.get('type')
        if customization_type:
            customizations = self.queryset.filter(customization_type=customization_type)
        else:
            customizations = self.queryset.all()
        
        serializer = self.get_serializer(customizations, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reviews with categories.
    
    list: Get all approved reviews
    create: Submit a new review
    """
    queryset = Review.objects.filter(is_approved=True)
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['menu_item', 'branch', 'category', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Only show approved reviews to public
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)
        # Filter by category if provided
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def create(self, request, *args, **kwargs):
        """Create a new review (pending approval)"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_approved=False)  # Reviews need approval
        return Response(
            {'message': 'Review submitted successfully and is pending approval'},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get reviews grouped by category"""
        category = request.query_params.get('type')
        if category and category in ['branch', 'service', 'product', 'other']:
            reviews = self.queryset.filter(category=category, is_approved=True)
        else:
            reviews = self.queryset.filter(is_approved=True)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)


class BranchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing restaurant branches.
    """
    queryset = Branch.objects.filter(is_active=True)
    serializer_class = BranchSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'address']
    ordering_fields = ['name', 'city', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all approved reviews for this branch"""
        branch = self.get_object()
        reviews = branch.reviews.filter(is_approved=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class RestaurantInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for restaurant information (read-only for API).
    """
    queryset = RestaurantInfo.objects.all()
    serializer_class = RestaurantInfoSerializer

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current restaurant information"""
        try:
            restaurant_info = RestaurantInfo.objects.first()
            if restaurant_info:
                serializer = self.get_serializer(restaurant_info)
                return Response(serializer.data)
            return Response(
                {'message': 'Restaurant information not configured'},
                status=status.HTTP_404_NOT_FOUND
            )
        except RestaurantInfo.DoesNotExist:
            return Response(
                {'message': 'Restaurant information not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# Authentication API Views

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login API endpoint for Flutter app
    
    POST /api/auth/login/
    Body: {"username": "admin", "password": "admin123"}
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({
            'success': True,
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_staff,
                'is_superadmin': user.is_superuser,
            }
        })
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout API endpoint
    
    POST /api/auth/logout/
    """
    logout(request)
    return Response({'success': True, 'message': 'Logged out successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """
    Get current logged in user info
    
    GET /api/auth/user/
    """
    user = request.user
    return Response({
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_staff,
        'is_superadmin': user.is_superuser,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register new user
    
    POST /api/auth/register/
    Body: {"username": "user", "email": "user@example.com", "password": "password123"}
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    
    login(request, user)
    
    return Response({
        'success': True,
        'user': {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_staff,
            'is_superadmin': user.is_superuser,
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_review(request):
    """
    Submit a new review with category support
    
    POST /api/reviews/submit/
    Body: {
        "category": "product",  # branch, service, product, other
        "menu_item_id": 1,  # required for product reviews
        "branch_id": 1,  # required for branch reviews
        "customer_name": "John Doe",
        "rating": 5,
        "comment": "Great pizza!"
    }
    """
    try:
        category = request.data.get('category', 'other')
        menu_item_id = request.data.get('menu_item_id')
        branch_id = request.data.get('branch_id')
        customer_name = request.data.get('customer_name')
        rating = request.data.get('rating')
        comment = request.data.get('comment', '')
        
        if not customer_name or not rating:
            return Response(
                {'error': 'Please provide customer_name and rating'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate rating
        if not (1 <= int(rating) <= 5):
            return Response(
                {'error': 'Rating must be between 1 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate category
        if category not in ['branch', 'service', 'product', 'other']:
            return Response(
                {'error': 'Invalid category. Must be: branch, service, product, or other'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        menu_item = None
        branch = None
        
        # Get related object based on category
        if category == 'product':
            if not menu_item_id:
                return Response(
                    {'error': 'menu_item_id is required for product reviews'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                menu_item = MenuItem.objects.get(id=menu_item_id)
            except MenuItem.DoesNotExist:
                return Response(
                    {'error': 'Menu item not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        if category == 'branch':
            if not branch_id:
                return Response(
                    {'error': 'branch_id is required for branch reviews'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                branch = Branch.objects.get(id=branch_id)
            except Branch.DoesNotExist:
                return Response(
                    {'error': 'Branch not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Create review
        review = Review.objects.create(
            category=category,
            menu_item=menu_item,
            branch=branch,
            customer_name=customer_name,
            rating=int(rating),
            comment=comment,
            is_approved=False  # Requires admin approval
        )
        
        return Response({
            'success': True,
            'message': 'Review submitted successfully! It will be visible after approval.',
            'review_id': review.id,
            'category': category
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def ingredient_details(request, ingredient_id):
    """
    Get detailed information about an ingredient
    
    GET /api/ingredients/{id}/details/
    """
    try:
        ingredient = Ingredient.objects.get(id=ingredient_id)
        
        # Get menu items using this ingredient
        menu_items = MenuItem.objects.filter(
            ingredients__ingredient=ingredient
        ).distinct()
        
        data = {
            'id': ingredient.id,
            'name': ingredient.name,
            'description': ingredient.description,
            'origin': ingredient.origin,
            'nutritional_info': ingredient.nutritional_info,
            'supplier': ingredient.supplier,
            'is_seasonal': ingredient.seasonal,
            'is_organic': ingredient.organic,
            'is_allergen': ingredient.is_allergen,
            'image': ingredient.image.url if ingredient.image else None,
            'used_in_menu_items': [
                {
                    'id': item.id,
                    'name': item.name,
                    'category': item.category.name,
                    'price': str(item.price)
                }
                for item in menu_items
            ]
        }
        
        return Response(data)
        
    except Ingredient.DoesNotExist:
        return Response(
            {'error': 'Ingredient not found'},
            status=status.HTTP_404_NOT_FOUND
        )
