@echo off
echo ====================================
echo CREATING SUPERADMIN ACCOUNT
echo ====================================
echo.

cd /d "c:\Users\oussa\OneDrive\Desktop\60 seconds to napoli"

set DJANGO_SETTINGS_MODULE=restaurant_api.settings

python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.filter(is_superuser=True).first() or User.objects.create_superuser('admin', 'admin@napoli.com', 'admin123'); user.username='admin'; user.email='admin@napoli.com'; user.set_password('admin123'); user.save(); print(''); print('='*50); print('SUPERADMIN LOGIN CREDENTIALS'); print('='*50); print('URL:      http://127.0.0.1:8000/admin/'); print('Username: admin'); print('Password: admin123'); print('='*50)"

echo.
echo ====================================
echo SUPERADMIN READY!
echo ====================================
echo.
pause
