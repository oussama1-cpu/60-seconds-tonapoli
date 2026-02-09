from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.utils.translation import gettext as _
from .models import MenuItem, Category, RestaurantInfo, Review, Ingredient

def home(request):
    """Display the homepage with featured items and restaurant information"""
    featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)[:3]
    restaurant_info = RestaurantInfo.objects.first()
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')[:6]
    
    context = {
        'featured_items': featured_items,
        'restaurant_info': restaurant_info,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)

def menu_page(request):
    """Display the full menu page"""
    categories = Category.objects.prefetch_related('items').filter(is_active=True)
    return render(request, 'menu/list.html', {'categories': categories})

def menu_item_detail(request, pk):
    """Display details for a specific menu item"""
    menu_item = get_object_or_404(MenuItem.objects.prefetch_related('ingredients__ingredient', 'reviews'), pk=pk, is_available=True)
    
    # Get related items from same category
    related_items = MenuItem.objects.filter(
        category=menu_item.category,
        is_available=True
    ).exclude(pk=menu_item.pk)[:3]
    
    context = {
        'menu_item': menu_item,
        'related_items': related_items,
    }
    return render(request, 'menu/detail.html', context)

def about(request):
    """Display the about page"""
    return render(request, 'about.html')

def checkout(request):
    """Display the checkout page"""
    # Check if cart has items
    cart_data = request.session.get('cart', [])
    if not cart_data:
        return redirect('menu-page')
    
    context = {
        'cart_items': cart_data,
    }
    return render(request, 'orders/checkout.html', context)

def order_confirmation(request, order_number):
    """Display order confirmation page"""
    # In a real app, you'd fetch the order from database
    order_data = {
        'order_number': order_number,
        'status': 'confirmed',
        'estimated_time': '25-35 minutes',
        'total': '0.00 €'
    }
    
    return render(request, 'orders/order_confirmation.html', order_data)

def order_tracking(request, order_number):
    """Display order tracking page"""
    # In a real app, you'd fetch the order from database
    order_data = {
        'order_number': order_number,
        'status': 'preparing',
        'estimated_time': '25-35 minutes',
        'current_step': 2,
        'steps': [
            {'name': 'Order Confirmed', 'completed': True, 'time': '12:30 PM'},
            {'name': 'Preparing', 'completed': True, 'time': '12:32 PM'},
            {'name': 'On the way', 'completed': False, 'time': 'Est. 12:45 PM'},
            {'name': 'Delivered', 'completed': False, 'time': 'Est. 12:50 PM'}
        ]
    }
    
    return render(request, 'orders/order_tracking.html', order_data)

def contact(request):
    """Display the contact page"""
    restaurant_info = RestaurantInfo.objects.first()
    return render(request, 'contact.html', {'restaurant_info': restaurant_info})


@csrf_exempt
@require_POST
def submit_review_frontend(request):
    """Handle review submission from frontend"""
    try:
        data = json.loads(request.body)
        
        menu_item_id = data.get('menu_item_id')
        customer_name = data.get('customer_name')
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if not menu_item_id or not customer_name or not rating:
            return JsonResponse({
                'success': False,
                'error': 'Please provide menu_item_id, customer_name, and rating'
            }, status=400)
        
        # Validate rating
        if not (1 <= int(rating) <= 5):
            return JsonResponse({
                'success': False,
                'error': 'Rating must be between 1 and 5'
            }, status=400)
        
        # Get menu item
        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Menu item not found'
            }, status=404)
        
        # Create review
        review = Review.objects.create(
            menu_item=menu_item,
            customer_name=customer_name,
            rating=int(rating),
            comment=comment,
            is_approved=False  # Requires admin approval
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Review submitted successfully! It will be visible after approval.',
            'review_id': review.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def ingredient_details_frontend(request, ingredient_id):
    """Get detailed ingredient information for frontend"""
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
        
        return JsonResponse(data)
        
    except Ingredient.DoesNotExist:
        return JsonResponse({
            'error': 'Ingredient not found'
        }, status=404)
