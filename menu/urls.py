from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, MenuItemViewSet, IngredientViewSet,
    CustomizationViewSet, ReviewViewSet, RestaurantInfoViewSet,
    BranchViewSet, login_view, logout_view, current_user_view,
    register_view, submit_review, ingredient_details
)
from .views_upload import upload_image

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'menu-items', MenuItemViewSet, basename='menuitem')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'customizations', CustomizationViewSet, basename='customization')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'restaurant-info', RestaurantInfoViewSet, basename='restaurantinfo')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-image/', upload_image, name='upload-image'),
    # Authentication endpoints
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/user/', current_user_view, name='current-user'),
    path('auth/register/', register_view, name='register'),
    # Enhanced features endpoints
    path('reviews/submit/', submit_review, name='submit-review'),
    path('ingredients/<int:ingredient_id>/details/', ingredient_details, name='ingredient-details'),
]
