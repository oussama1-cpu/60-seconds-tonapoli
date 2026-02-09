"""
URL configuration for restaurant_api project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from menu.views_frontend import (
    home, menu_page, menu_item_detail, about, contact,
    checkout, order_confirmation, order_tracking,
    submit_review_frontend, ingredient_details_frontend
)
from menu.views_auth import (
    login_page, register_page, logout_page, account_page,
    update_profile, change_password
)

# Swagger/OpenAPI documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Restaurant Menu API",
      default_version='v1',
      description="API for restaurant menu management system",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@restaurant.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin and API URLs (non-internationalized)
    path('admin/', admin.site.urls),
    path('api/', include('menu.urls')),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Language switching
    path('i18n/', include('django.conf.urls.i18n')),
    
    # Static and media files
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Internationalized URL patterns
urlpatterns += i18n_patterns(
    # Frontend URLs
    path('', home, name='home'),
    path('menu/', menu_page, name='menu-list'),
    path('menu/item/<int:pk>/', menu_item_detail, name='menu-item-detail'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    
    # Authentication URLs
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('account/', account_page, name='account'),
    path('account/update-profile/', update_profile, name='update-profile'),
    path('account/change-password/', change_password, name='change-password'),
    
    # Frontend API endpoints
    path('checkout/', checkout, name='checkout'),
    path('order-confirmation/<str:order_number>/', order_confirmation, name='order-confirmation'),
    path('order-tracking/<str:order_number>/', order_tracking, name='order-tracking'),
    path('submit-review/', submit_review_frontend, name='submit-review-frontend'),
    path('ingredient/<int:ingredient_id>/', ingredient_details_frontend, name='ingredient-details-frontend'),
    
    # Language prefix will be automatically added (e.g., /en/, /ar/)
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "Restaurant Menu Administration"
admin.site.site_title = "Restaurant Menu Admin"
admin.site.index_title = "Welcome to Restaurant Menu Management"
