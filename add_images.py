import os
import django
import requests
from django.core.files.base import ContentFile

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_api.settings')
django.setup()

from menu.models import MenuItem, Ingredient

def add_food_images():
    """Add food images from internet to menu items and ingredients"""
    
    # Food image URLs by category
    food_images = {
        'pizza': [
            'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1594007654729-407eedc4be65?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1604382355076-af4b026608f8?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800&h=600&fit=crop',
        ],
        'pasta': [
            'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1563379091339-03246963d272?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=800&h=600&fit=crop',
        ],
        'salad': [
            'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=800&h=600&fit=crop',
        ],
        'dessert': [
            'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1563729784474-d77dbb933a9f?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1551024601-bec78aea704b?w=800&h=600&fit=crop',
        ],
        'drink': [
            'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1533473359338-0505a3d8b915?w=800&h=600&fit=crop',
        ],
        'appetizer': [
            'https://images.unsplash.com/photo-1529042410759-b140b76779e6?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800&h=600&fit=crop',
        ]
    }

    # Ingredient images
    ingredient_images = {
        'tomato': 'https://images.unsplash.com/photo-1546470427-e92b2c9c09d6?w=400&h=400&fit=crop',
        'cheese': 'https://images.unsplash.com/photo-1486477181946-76b2e7d14cf1?w=400&h=400&fit=crop',
        'basil': 'https://images.unsplash.com/photo-1592616352834-bd5828474f8c?w=400&h=400&fit=crop',
        'olive': 'https://images.unsplash.com/photo-1525373612132-b3e820b87cea?w=400&h=400&fit=crop',
        'mushroom': 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=400&h=400&fit=crop',
        'pepper': 'https://images.unsplash.com/photo-1583221552368-2e937063fb23?w=400&h=400&fit=crop',
        'onion': 'https://images.unsplash.com/photo-1590502593747-42a996133562?w=400&h=400&fit=crop',
        'garlic': 'https://images.unsplash.com/photo-1574393344493-8975dd99e9c2?w=400&h=400&fit=crop',
        'flour': 'https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=400&h=400&fit=crop',
        'meat': 'https://images.unsplash.com/photo-1529692236671-f1f6cf96834a?w=400&h=400&fit=crop',
    }

    print('Adding food images to menu items...')
    
    # Add images to menu items
    menu_items_updated = 0
    for item in MenuItem.objects.all():
        if item.image:
            print(f'Skipping {item.name} - already has image')
            continue

        # Determine category for image selection
        category_name = item.category.name.lower()
        image_urls = []
        
        # Map category to image URLs
        if 'pizza' in category_name:
            image_urls = food_images['pizza']
        elif 'pasta' in category_name:
            image_urls = food_images['pasta']
        elif 'salad' in category_name:
            image_urls = food_images['salad']
        elif 'dessert' in category_name or 'sweet' in category_name:
            image_urls = food_images['dessert']
        elif 'drink' in category_name or 'beverage' in category_name:
            image_urls = food_images['drink']
        elif 'appetizer' in category_name or 'starter' in category_name:
            image_urls = food_images['appetizer']
        else:
            # Default to pizza images
            image_urls = food_images['pizza']

        # Select image based on item ID for consistency
        if image_urls:
            image_url = image_urls[item.id % len(image_urls)]
            
            try:
                response = requests.get(image_url, timeout=10)
                response.raise_for_status()
                
                # Get file extension from URL or default to .jpg
                file_ext = '.jpg'
                if '.' in image_url.split('/')[-1]:
                    file_ext = '.' + image_url.split('.')[-1].split('?')[0]
                
                # Save image
                filename = f"{item.name.lower().replace(' ', '_').replace('/', '_')}{file_ext}"
                item.image.save(filename, ContentFile(response.content), save=True)
                menu_items_updated += 1
                
                print(f'✓ Added image to {item.name}')
                
            except Exception as e:
                print(f'✗ Failed to add image to {item.name}: {str(e)}')

    # Add images to ingredients
    ingredients_updated = 0
    print('\nAdding images to ingredients...')
    
    for ingredient in Ingredient.objects.all():
        if ingredient.image:
            print(f'Skipping {ingredient.name} - already has image')
            continue

        # Find matching ingredient image
        ingredient_name = ingredient.name.lower()
        image_url = None
        
        for key, url in ingredient_images.items():
            if key in ingredient_name:
                image_url = url
                break
        
        if image_url:
            try:
                response = requests.get(image_url, timeout=10)
                response.raise_for_status()
                
                filename = f"{ingredient.name.lower().replace(' ', '_').replace('/', '_')}.jpg"
                ingredient.image.save(filename, ContentFile(response.content), save=True)
                ingredients_updated += 1
                
                print(f'✓ Added image to {ingredient.name}')
                
            except Exception as e:
                print(f'✗ Failed to add image to {ingredient.name}: {str(e)}')

    print(f'\n✓ Complete! Updated {menu_items_updated} menu items and {ingredients_updated} ingredients with images.')

if __name__ == '__main__':
    add_food_images()
