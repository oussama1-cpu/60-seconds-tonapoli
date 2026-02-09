@echo off
echo Populating database with sample data...
echo.
call venv\Scripts\activate.bat
python -c "exec(open('sample_data.py').read())"
echo.
echo Done!
pause
