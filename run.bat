@echo off
echo Starting Restaurant Menu API Server...
echo.
call venv\Scripts\activate.bat
python manage.py runserver
