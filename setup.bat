@echo off
REM Setup script for MIC Radiology Management System (Windows)

echo MIC Radiology Management System - Setup
echo ========================================

echo Checking Python version...
python --version

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo ^! Please update .env with your settings!
)

echo Running migrations...
python manage.py makemigrations
python manage.py migrate

echo Creating superuser...
python manage.py createsuperuser

echo Initializing scan types and medical aids...
python manage.py init_data

echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo Setup complete!
echo.
echo To start the development server, run:
echo python manage.py runserver
echo.
echo Admin panel: http://localhost:8000/admin/
