@echo off
echo ========================================
echo Restaurant Menu API - Setup Script
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo Please edit .env file and set your SECRET_KEY
)

echo.
echo Creating media directories...
if not exist media mkdir media
if not exist media\categories mkdir media\categories
if not exist media\menu_items mkdir media\menu_items
if not exist media\restaurant mkdir media\restaurant

echo.
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and set a strong SECRET_KEY
echo 2. Create a superuser: python manage.py createsuperuser
echo 3. Run the server: python manage.py runserver
echo 4. Access admin at: http://127.0.0.1:8000/admin/
echo 5. View API docs at: http://127.0.0.1:8000/swagger/
echo.
pause
