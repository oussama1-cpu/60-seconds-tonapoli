# 🚀 Getting Started - Restaurant Menu API

## Welcome!

This is your complete Django REST API for restaurant menu management. Everything is ready to use!

## 📦 What You Have

✅ **Django REST API** - Complete backend with all endpoints  
✅ **Admin Dashboard** - Beautiful interface for managing your menu  
✅ **Database Models** - Categories, Menu Items, Ingredients, Reviews, etc.  
✅ **API Documentation** - Auto-generated Swagger/ReDoc docs  
✅ **Flutter Ready** - CORS enabled and ready for mobile integration  
✅ **Sample Data Script** - Quick way to populate your database  
✅ **Complete Documentation** - Multiple guides for different needs  

## ⚡ Quick Start (3 Steps)

### Step 1: Setup (5 minutes)
```bash
# Double-click setup.bat (Windows)
# OR run manually:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Create Admin Account
```bash
python manage.py createsuperuser
```
Enter your username, email, and password when prompted.

### Step 3: Start Server
```bash
# Double-click run.bat
# OR run:
python manage.py runserver
```

## 🎯 Access Your Application

Once the server is running:

| What | URL | Description |
|------|-----|-------------|
| **Admin Dashboard** | http://127.0.0.1:8000/admin/ | Manage your menu |
| **API Root** | http://127.0.0.1:8000/api/ | API endpoints |
| **Swagger Docs** | http://127.0.0.1:8000/swagger/ | Interactive API docs |
| **ReDoc** | http://127.0.0.1:8000/redoc/ | Alternative API docs |

## 📝 First Tasks

### 1. Add Restaurant Information
1. Go to Admin Dashboard
2. Click "Restaurant Information"
3. Click "Add Restaurant Information"
4. Fill in your restaurant details
5. Save

### 2. Create Categories
1. Click "Categories" in admin
2. Click "Add Category"
3. Add categories like: Appetizers, Main Courses, Desserts, Drinks
4. Set order numbers (1, 2, 3, etc.)
5. Upload images (optional)

### 3. Add Menu Items
1. Click "Menu Items" in admin
2. Click "Add Menu Item"
3. Fill in details:
   - Name and description
   - Select category
   - Set price
   - Upload image
   - Mark dietary options (vegetarian, vegan, etc.)
   - Set availability
4. Save

### 4. OR Use Sample Data
```bash
python manage.py shell
>>> exec(open('sample_data.py').read())
```
This creates sample Italian restaurant menu with 20+ items!

## 📱 Connect Flutter App

In your Flutter app, use:

```dart
// Android Emulator
static const String baseUrl = 'http://10.0.2.2:8000/api';

// iOS Simulator  
static const String baseUrl = 'http://localhost:8000/api';

// Physical Device (replace with your IP)
static const String baseUrl = 'http://192.168.1.XXX:8000/api';
```

See **FLUTTER_INTEGRATION.md** for complete Flutter code examples.

## 🧪 Test the API

### Using Browser
Visit: http://127.0.0.1:8000/api/categories/

### Using Swagger
1. Go to: http://127.0.0.1:8000/swagger/
2. Try the "GET /api/categories/" endpoint
3. Click "Try it out" → "Execute"

### Using curl
```bash
curl http://127.0.0.1:8000/api/categories/
curl http://127.0.0.1:8000/api/menu-items/
curl http://127.0.0.1:8000/api/restaurant-info/current/
```

## 📚 Documentation

Choose the guide that fits your needs:

| Document | Best For |
|----------|----------|
| **QUICKSTART.md** | Getting started in 5 minutes |
| **README.md** | Complete documentation and reference |
| **FLUTTER_INTEGRATION.md** | Flutter developers |
| **PROJECT_OVERVIEW.md** | Understanding the architecture |
| **GETTING_STARTED.md** | This file - first-time setup |

## 🔧 Common Commands

```bash
# Activate virtual environment
venv\Scripts\activate

# Run server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Create migrations (after model changes)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test menu

# Load sample data
python manage.py shell
>>> exec(open('sample_data.py').read())

# Django shell (for testing)
python manage.py shell
```

## 🎨 Admin Dashboard Features

Your admin dashboard includes:

- ✅ **Visual Interface** - Image previews, color-coded badges
- ✅ **Inline Editing** - Edit prices, availability without opening items
- ✅ **Bulk Actions** - Update multiple items at once
- ✅ **Advanced Filters** - Filter by category, dietary options, etc.
- ✅ **Search** - Find items quickly
- ✅ **Drag & Drop** - Reorder items (via order field)
- ✅ **Review Moderation** - Approve/reject customer reviews

## 🌐 API Endpoints Quick Reference

```
Categories
  GET    /api/categories/              List all
  GET    /api/categories/{id}/         Get one
  GET    /api/categories/{id}/items/   Items in category

Menu Items
  GET    /api/menu-items/              List all
  GET    /api/menu-items/{id}/         Get details
  GET    /api/menu-items/featured/     Featured items
  GET    /api/menu-items/search/?q=    Search

Filters
  ?category=1                           By category
  ?is_vegetarian=true                   Vegetarian only
  ?is_vegan=true                        Vegan only
  ?price__gte=10&price__lte=20         Price range

Reviews
  GET    /api/reviews/                 List reviews
  POST   /api/reviews/                 Submit review

Restaurant
  GET    /api/restaurant-info/current/ Get info
```

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if Python is installed
python --version

# Check if port 8000 is in use
netstat -ano | findstr :8000

# Use different port
python manage.py runserver 8080
```

### Can't login to admin
```bash
# Create new superuser
python manage.py createsuperuser
```

### Images not showing
```bash
# Create media directories
mkdir media\categories
mkdir media\menu_items
mkdir media\restaurant
```

### Module not found errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Database errors
```bash
# Reset database (WARNING: deletes all data)
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## 🎓 Learning Resources

### Django
- Official Docs: https://docs.djangoproject.com/
- Tutorial: https://docs.djangoproject.com/en/4.2/intro/tutorial01/

### Django REST Framework
- Official Docs: https://www.django-rest-framework.org/
- Tutorial: https://www.django-rest-framework.org/tutorial/quickstart/

### Flutter HTTP
- Package: https://pub.dev/packages/http
- Tutorial: https://flutter.dev/docs/cookbook/networking/fetch-data

## 💡 Tips

1. **Use Sample Data** - Run `sample_data.py` to get started quickly
2. **Test in Swagger** - Interactive API testing is easier than curl
3. **Check Admin First** - Verify data in admin before testing API
4. **Use Filters** - API supports extensive filtering options
5. **Read Error Messages** - Django provides helpful error details

## 🚀 Next Steps

1. ✅ Complete setup
2. ✅ Create admin account
3. ✅ Add restaurant info
4. ✅ Add menu items (or use sample data)
5. ✅ Test API endpoints
6. ✅ Connect Flutter app
7. ✅ Deploy to production (when ready)

## 📞 Need Help?

1. Check the documentation files
2. Review error messages carefully
3. Test in Swagger UI
4. Check Django/DRF documentation
5. Verify your environment setup

## ✨ You're All Set!

Your restaurant menu API is ready to use. Start by:
1. Running the server
2. Logging into admin
3. Adding your menu
4. Testing the API
5. Connecting your Flutter app

**Happy coding! 🎉**
