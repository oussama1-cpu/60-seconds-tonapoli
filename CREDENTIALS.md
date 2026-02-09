# 🔐 Complete Credentials Guide - 60 Seconds to Napoli

## ✅ SUPER ADMIN CREDENTIALS (Use These!)

### For Django Admin Panel (Backend Management)
```
URL:      http://127.0.0.1:8000/admin/
Username: admin
Password: admin123
```

**What you can do:**
- ✅ Manage Categories
- ✅ Manage Menu Items
- ✅ Manage Ingredients
- ✅ Manage Customizations
- ✅ Approve Reviews
- ✅ Manage Restaurant Info
- ✅ Create/Delete Users
- ✅ Full database access

---

### For Flutter Mobile App (Frontend)
```
Username: admin
Password: admin123
```

**What you can do:**
- ✅ Access Admin Panel from mobile
- ✅ Menu CRUD (Create/Update/Delete items)
- ✅ Add reviews
- ✅ All user features
- ✅ AI Chat assistant
- ✅ Super admin dashboard

---

## 📊 How Authentication Works Now

### Before (❌ Old System - Don't Use)
- Flutter had local hardcoded credentials
- `superadmin/napoli2024secure` only worked in Flutter
- No connection to Django backend
- Data not synced

### After (✅ New System - Use This!)
- Flutter authenticates against Django backend
- Django validates credentials and returns user info
- Same admin account works everywhere
- Full integration between frontend and backend

---

## 🔄 Authentication Flow

```
1. User enters credentials in Flutter app
   ↓
2. Flutter calls: POST http://127.0.0.1:8000/api/auth/login/
   Body: {"username": "admin", "password": "admin123"}
   ↓
3. Django validates credentials
   ↓
4. Django returns user info:
   {
     "success": true,
     "user": {
       "id": "1",
       "username": "admin",
       "email": "admin@napoli.com",
       "is_admin": true,
       "is_superadmin": true
     }
   }
   ↓
5. Flutter stores user data locally
   ↓
6. User is logged in with admin privileges
```

---

## 🚀 Step-by-Step: How to Use

### Step 1: Start Django Backend
```bash
cd "c:\Users\oussa\OneDrive\Desktop\60 seconds to napoli"
python manage.py runserver
```
Backend will run on: http://127.0.0.1:8000

### Step 2: Start Flutter App
```bash
cd "c:\Users\oussa\OneDrive\Desktop\napoli_menu_app"
flutter run -d chrome
```
App will open in Chrome browser

### Step 3: Login to Flutter App
1. Click "Login" button in Quick Access section
2. Enter credentials:
   - Username: `admin`
   - Password: `admin123`
3. Click "Login"

### Step 4: Access Admin Features
After login, you'll see:
- 🛠️ Admin Panel icon (top right)
- Admin options in profile menu
- Full admin controls

---

## 🌐 API Endpoints

### Authentication Endpoints
```
POST   /api/auth/login/      - Login with username/password
POST   /api/auth/logout/     - Logout current user
GET    /api/auth/user/       - Get current user info
POST   /api/auth/register/   - Register new user
```

### Menu Endpoints
```
GET    /api/categories/              - List all categories
GET    /api/menu-items/              - List all menu items
GET    /api/menu-items/{id}/         - Get item details
POST   /api/menu-items/              - Create item (admin only)
PUT    /api/menu-items/{id}/         - Update item (admin only)
DELETE /api/menu-items/{id}/         - Delete item (admin only)
GET    /api/menu-items/featured/     - Get featured items
GET    /api/menu-items/search/?q=    - Search items
```

### Other Endpoints
```
GET    /api/ingredients/             - List ingredients
GET    /api/customizations/          - List customizations
GET    /api/reviews/                 - List reviews
POST   /api/reviews/                 - Submit review
GET    /api/restaurant-info/current/ - Get restaurant info
```

---

## 🔧 Testing Authentication

### Test Login via cURL (Command Line)
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

### Expected Response
```json
{
  "success": true,
  "user": {
    "id": "1",
    "username": "admin",
    "email": "admin@napoli.com",
    "is_admin": true,
    "is_superadmin": true
  }
}
```

---

## 👥 User Types

### Super Admin (admin/admin123)
- **Django Access:** ✅ Full admin panel
- **Flutter Access:** ✅ All features + admin controls
- **Can Create/Edit/Delete:** ✅ Everything
- **Manage Users:** ✅ Yes

### Regular Users (signup required)
- **Django Access:** ❌ No admin panel
- **Flutter Access:** ✅ Browse menu, add reviews
- **Can Create/Edit/Delete:** ❌ No
- **Manage Users:** ❌ No

### Guest Mode (no login)
- **Django Access:** ❌ No
- **Flutter Access:** ✅ Browse menu only
- **Can Create/Edit/Delete:** ❌ No
- **Manage Users:** ❌ No

---

## 📝 Creating Additional Admin Users

### Method 1: Django Admin Panel
1. Go to: http://127.0.0.1:8000/admin/
2. Login with admin/admin123
3. Click "Users" → "Add User"
4. Fill in username and password
5. Check "Staff status" and "Superuser status"
6. Save

### Method 2: Command Line
```bash
cd "c:\Users\oussa\OneDrive\Desktop\60 seconds to napoli"
python manage.py createsuperuser
```
Follow prompts to create new admin user

### Method 3: Python Script
```python
from django.contrib.auth.models import User

User.objects.create_superuser(
    username='newadmin',
    email='newadmin@napoli.com',
    password='securepass123'
)
```

---

## 🔒 Security Notes

### Development (Current Setup)
- ✅ DEBUG = True
- ✅ CORS_ALLOW_ALL_ORIGINS = True
- ✅ Simple password (admin123)
- ❌ Not suitable for production

### Production Checklist
- [ ] Set DEBUG = False
- [ ] Change admin password to strong password
- [ ] Configure specific CORS_ALLOWED_ORIGINS
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Use environment variables for secrets
- [ ] Set SESSION_COOKIE_SECURE = True
- [ ] Set CSRF_COOKIE_SECURE = True
- [ ] Use PostgreSQL/MySQL instead of SQLite
- [ ] Enable Django security middleware
- [ ] Add rate limiting
- [ ] Enable logging and monitoring

---

## 🆘 Troubleshooting

### Problem: Login fails in Flutter app
**Solution:**
1. Make sure Django backend is running (port 8000)
2. Check credentials are exactly: admin / admin123
3. Check browser console for errors
4. Verify API endpoint: http://127.0.0.1:8000/api/auth/login/

### Problem: "CORS error" in browser console
**Solution:**
1. Django backend should have CORS enabled (already configured)
2. Restart Django server if you changed settings
3. Clear browser cache

### Problem: Admin features not showing after login
**Solution:**
1. Make sure you logged out and logged back in
2. Check that is_admin = true in API response
3. Try hot restart in Flutter (press 'R' in terminal)

### Problem: Can't access Django admin panel
**Solution:**
1. Go to: http://127.0.0.1:8000/admin/
2. Use credentials: admin / admin123
3. If credentials don't work, run create_admin.bat

---

## 📞 Quick Reference

| What | Where | Credentials |
|------|-------|-------------|
| **Django Admin** | http://127.0.0.1:8000/admin/ | admin / admin123 |
| **Flutter App** | http://localhost:8080 (or Chrome) | admin / admin123 |
| **API Root** | http://127.0.0.1:8000/api/ | - |
| **Login Endpoint** | POST /api/auth/login/ | admin / admin123 |

---

## ✅ Verification Checklist

Test everything is working:

- [ ] Django server running on port 8000
- [ ] Flutter app running in browser
- [ ] Can login with admin/admin123 in Flutter app
- [ ] Admin panel icon appears after login
- [ ] Can access Django admin panel
- [ ] Can add/edit menu items from Django admin
- [ ] Menu items appear in Flutter app
- [ ] Can add reviews in Flutter app

**If all checkboxes are checked ✅ - Everything is working perfectly!**

---

**Last Updated:** 2024
**System:** Fully Integrated Django + Flutter Authentication
