# Restaurant Menu Digitalization API

A comprehensive Django REST API for managing restaurant menus with a powerful admin dashboard. Perfect for integration with Flutter mobile applications.

## Features

### 🎯 Core Features
- **Complete Menu Management**: Categories, menu items, ingredients, and customizations
- **Rich Admin Dashboard**: Full CRUD operations with beautiful UI
- **RESTful API**: Well-documented endpoints for Flutter integration
- **Image Support**: Upload and manage images for categories and menu items
- **Advanced Filtering**: Search, filter by dietary preferences, price range, etc.
- **Review System**: Customer reviews with moderation
- **Restaurant Info**: Manage restaurant details, hours, and social media

### 🍽️ Menu Features
- Categories with ordering and images
- Detailed menu items with:
  - Pricing and images
  - Dietary information (vegetarian, vegan, gluten-free, nuts)
  - Spice levels
  - Preparation time and calories
  - Availability status
  - Featured items
- Ingredient tracking with allergen marking
- Customization options (sizes, extras, sauces, sides)

### 📊 Admin Dashboard Features
- Beautiful, intuitive interface
- Inline editing for quick updates
- Image previews
- Bulk actions
- Advanced filtering and search
- Visual dietary badges
- Review moderation

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or navigate to the project directory**
```bash
cd "c:\Users\oussa\OneDrive\Desktop\60 seconds to napoli"
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Create environment file**
```bash
copy .env.example .env
```

Edit `.env` and set your configuration:
```
SECRET_KEY=your-secret-key-here-generate-a-strong-one
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

6. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser (admin account)**
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

8. **Create media directories**
```bash
mkdir media
mkdir media\categories
mkdir media\menu_items
mkdir media\restaurant
```

9. **Run the development server**
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## Usage

### Admin Dashboard
Access the admin dashboard at: `http://127.0.0.1:8000/admin/`

Login with the superuser credentials you created.

#### Admin Features:
1. **Categories**: Create and organize menu categories
2. **Menu Items**: Add items with full details, images, and dietary info
3. **Ingredients**: Manage ingredients and mark allergens
4. **Customizations**: Create size options, extras, and add-ons
5. **Reviews**: Moderate customer reviews
6. **Restaurant Info**: Set up restaurant details (only one instance allowed)

### API Documentation
- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`

### API Endpoints

#### Base URL: `http://127.0.0.1:8000/api/`

#### Categories
- `GET /api/categories/` - List all categories
- `GET /api/categories/{id}/` - Get category details
- `GET /api/categories/{id}/items/` - Get all items in category
- `POST /api/categories/` - Create category (admin)
- `PUT /api/categories/{id}/` - Update category (admin)
- `DELETE /api/categories/{id}/` - Delete category (admin)

#### Menu Items
- `GET /api/menu-items/` - List all menu items
- `GET /api/menu-items/{id}/` - Get item details with ingredients, reviews
- `GET /api/menu-items/featured/` - Get featured items
- `GET /api/menu-items/search/?q=pizza` - Search menu items
- `POST /api/menu-items/` - Create item (admin)
- `PUT /api/menu-items/{id}/` - Update item (admin)
- `DELETE /api/menu-items/{id}/` - Delete item (admin)

**Filters:**
- `?category=1` - Filter by category
- `?is_vegetarian=true` - Vegetarian items only
- `?is_vegan=true` - Vegan items only
- `?is_gluten_free=true` - Gluten-free items only
- `?is_featured=true` - Featured items only
- `?spice_level=hot` - Filter by spice level
- `?price__gte=10&price__lte=20` - Price range
- `?search=pasta` - Search in name/description

#### Ingredients
- `GET /api/ingredients/` - List all ingredients
- `GET /api/ingredients/allergens/` - Get allergen ingredients
- `POST /api/ingredients/` - Create ingredient (admin)

#### Customizations
- `GET /api/customizations/` - List all customizations
- `GET /api/customizations/by_type/?type=size` - Filter by type
- `POST /api/customizations/` - Create customization (admin)

#### Reviews
- `GET /api/reviews/` - List approved reviews
- `GET /api/reviews/?menu_item=1` - Reviews for specific item
- `POST /api/reviews/` - Submit a review (pending approval)

#### Restaurant Info
- `GET /api/restaurant-info/current/` - Get restaurant information

### Example API Responses

**Menu Item Detail:**
```json
{
  "id": 1,
  "name": "Margherita Pizza",
  "description": "Classic Italian pizza with tomato, mozzarella, and basil",
  "category": {
    "id": 1,
    "name": "Pizzas",
    "image": "/media/categories/pizza.jpg"
  },
  "price": "12.99",
  "image": "/media/menu_items/margherita.jpg",
  "spice_level": "none",
  "is_vegetarian": true,
  "is_vegan": false,
  "is_gluten_free": false,
  "is_available": true,
  "is_featured": true,
  "preparation_time": 15,
  "calories": 800,
  "ingredients": [
    {
      "ingredient": {
        "name": "Mozzarella",
        "is_allergen": true
      },
      "quantity": "200g",
      "is_optional": false
    }
  ],
  "customizations": [
    {
      "name": "Extra Cheese",
      "customization_type": "extra",
      "price_modifier": "2.00"
    }
  ],
  "average_rating": 4.5,
  "review_count": 12
}
```

## Flutter Integration

### Setup in Flutter

1. **Add dependencies to `pubspec.yaml`:**
```yaml
dependencies:
  http: ^1.1.0
  provider: ^6.0.5
```

2. **Create API service:**
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class MenuApiService {
  static const String baseUrl = 'http://10.0.2.2:8000/api'; // Android emulator
  // Use 'http://localhost:8000/api' for iOS simulator
  
  Future<List<dynamic>> getCategories() async {
    final response = await http.get(Uri.parse('$baseUrl/categories/'));
    if (response.statusCode == 200) {
      return json.decode(response.body)['results'];
    }
    throw Exception('Failed to load categories');
  }
  
  Future<List<dynamic>> getMenuItems({int? categoryId}) async {
    String url = '$baseUrl/menu-items/';
    if (categoryId != null) {
      url += '?category=$categoryId';
    }
    final response = await http.get(Uri.parse(url));
    if (response.statusCode == 200) {
      return json.decode(response.body)['results'];
    }
    throw Exception('Failed to load menu items');
  }
  
  Future<Map<String, dynamic>> getMenuItem(int id) async {
    final response = await http.get(Uri.parse('$baseUrl/menu-items/$id/'));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    }
    throw Exception('Failed to load menu item');
  }
}
```

### CORS Configuration
The API is configured to accept requests from Flutter apps. In production, update `CORS_ALLOWED_ORIGINS` in `settings.py`.

## Project Structure

```
60 seconds to napoli/
├── restaurant_api/          # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Main settings
│   ├── urls.py             # URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── menu/                    # Menu app
│   ├── migrations/         # Database migrations
│   ├── __init__.py
│   ├── admin.py           # Admin dashboard configuration
│   ├── apps.py
│   ├── models.py          # Database models
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   └── urls.py            # API URLs
├── media/                  # Uploaded images
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .env.example          # Environment template
├── .gitignore
└── README.md             # This file
```

## Database Models

### Category
- Name, description, image
- Display order
- Active status

### MenuItem
- Name, description, price, image
- Category relationship
- Dietary flags (vegetarian, vegan, gluten-free, nuts)
- Spice level
- Availability and featured status
- Preparation time and calories

### Ingredient
- Name, description
- Allergen flag

### Customization
- Name, type (size, extra, side, sauce)
- Price modifier
- Associated menu items

### Review
- Customer name, rating (1-5), comment
- Approval status

### RestaurantInfo
- Restaurant details
- Contact information
- Opening hours
- Social media links
- Currency and tax settings

## Development Tips

### Adding Sample Data
Use the admin dashboard to add your menu data, or create a management command:

```bash
python manage.py shell
```

```python
from menu.models import Category, MenuItem

# Create a category
category = Category.objects.create(
    name="Pizzas",
    description="Traditional Italian pizzas",
    order=1
)

# Create a menu item
MenuItem.objects.create(
    name="Margherita",
    description="Classic pizza with tomato and mozzarella",
    category=category,
    price=12.99,
    is_vegetarian=True,
    is_available=True
)
```

### Running Tests
```bash
python manage.py test menu
```

### Collecting Static Files (for production)
```bash
python manage.py collectstatic
```

## Production Deployment

Before deploying to production:

1. Set `DEBUG=False` in `.env`
2. Generate a strong `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` properly
4. Use a production database (PostgreSQL recommended)
5. Set up proper media file storage (AWS S3, etc.)
6. Configure HTTPS
7. Update CORS settings for your Flutter app domain

## Troubleshooting

### Images not showing
- Ensure media directories exist
- Check `MEDIA_URL` and `MEDIA_ROOT` in settings
- Verify file permissions

### CORS errors from Flutter
- Check `CORS_ALLOWED_ORIGINS` in settings.py
- Ensure your Flutter app URL is listed

### Admin styles not loading
```bash
python manage.py collectstatic
```

## Support

For issues or questions, please check:
- Django documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Flutter HTTP package: https://pub.dev/packages/http

## License

This project is open source and available for educational and commercial use.

---

**Happy Coding! 🚀**
