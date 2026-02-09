# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Automated Setup (Recommended for Windows)

1. **Double-click `setup.bat`**
   - This will automatically set up everything for you

2. **Create admin account:**
   ```bash
   venv\Scripts\activate
   python manage.py createsuperuser
   ```

3. **Start the server:**
   - Double-click `run.bat` OR
   - Run: `python manage.py runserver`

4. **Access the application:**
   - Admin Dashboard: http://127.0.0.1:8000/admin/
   - API Documentation: http://127.0.0.1:8000/swagger/

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Create media folders
mkdir media\categories media\menu_items media\restaurant

# 8. Run server
python manage.py runserver
```

## 📝 First Steps After Setup

### 1. Login to Admin Dashboard
- Go to: http://127.0.0.1:8000/admin/
- Login with your superuser credentials

### 2. Set Up Restaurant Information
- Click on "Restaurant Information"
- Add your restaurant details
- Upload logo
- Set opening hours and contact info

### 3. Create Categories
- Click on "Categories"
- Add categories like:
  - Appetizers
  - Main Courses
  - Pizzas
  - Pasta
  - Desserts
  - Drinks

### 4. Add Menu Items
- Click on "Menu Items"
- Add your dishes with:
  - Name and description
  - Category
  - Price
  - Image
  - Dietary information
  - Availability

### 5. Test the API
- Go to: http://127.0.0.1:8000/swagger/
- Try the endpoints:
  - GET /api/categories/
  - GET /api/menu-items/
  - GET /api/restaurant-info/current/

## 🔧 Common Commands

```bash
# Activate virtual environment
venv\Scripts\activate

# Run development server
python manage.py runserver

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

## 📱 Connect Your Flutter App

In your Flutter app, use this base URL:

```dart
// For Android Emulator
static const String baseUrl = 'http://10.0.2.2:8000/api';

// For iOS Simulator
static const String baseUrl = 'http://localhost:8000/api';

// For Physical Device (replace with your computer's IP)
static const String baseUrl = 'http://192.168.1.XXX:8000/api';
```

## 🎯 API Endpoints Quick Reference

```
GET  /api/categories/                    - List all categories
GET  /api/categories/{id}/items/         - Items in category
GET  /api/menu-items/                    - List all menu items
GET  /api/menu-items/{id}/               - Item details
GET  /api/menu-items/featured/           - Featured items
GET  /api/menu-items/search/?q=pizza     - Search items
GET  /api/restaurant-info/current/       - Restaurant info
POST /api/reviews/                       - Submit review
```

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Use different port
python manage.py runserver 8080
```

### Can't access from Flutter app
1. Make sure Django server is running
2. Check your device/emulator can reach your computer
3. Update CORS settings if needed
4. Use correct IP address for physical devices

### Images not showing
```bash
# Create media directories
mkdir media\categories media\menu_items media\restaurant
```

### Admin styles missing
```bash
python manage.py collectstatic
```

## 📚 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the [Swagger API docs](http://127.0.0.1:8000/swagger/)
3. Customize models in `menu/models.py`
4. Add custom API endpoints in `menu/views.py`
5. Modify admin interface in `menu/admin.py`

## 🎉 You're Ready!

Your restaurant menu API is now running and ready to be integrated with your Flutter app!

Need help? Check the README.md for more detailed information.
