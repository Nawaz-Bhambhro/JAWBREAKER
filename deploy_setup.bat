@echo off
REM Quick deployment setup script for Windows

echo 🚀 Django Healthcare API - Deployment Setup
echo ==========================================

REM Check if Git is initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
    echo Git repository initialized!
)

REM Install production dependencies
echo Installing production dependencies...
pip install -r requirements.txt

REM Create environment file
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env file with your actual values!
)

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Check for migrations
echo Checking for database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo Do you want to create a superuser? (y/n)
set /p create_superuser=
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your production values
echo 2. Push your code to GitHub/GitLab
echo 3. Deploy to your chosen platform (Railway, Heroku, etc.)
echo 4. Set environment variables in your deployment platform
echo 5. Test your deployed API
echo.
echo For detailed instructions, see DEPLOYMENT_GUIDE.md
echo.
echo 🎉 Your Django Healthcare API is ready for deployment!
pause
