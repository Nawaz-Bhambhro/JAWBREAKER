#!/bin/bash
# Quick deployment setup script

echo "🚀 Django Healthcare API - Deployment Setup"
echo "=========================================="

# Check if Git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    echo "Git repository initialized!"
fi

# Install production dependencies
echo "Installing production dependencies..."
pip install -r requirements.txt

# Create environment file
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual values!"
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Check for migrations
echo "Checking for database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if needed
echo "Do you want to create a superuser? (y/n)"
read -r create_superuser
if [[ $create_superuser == "y" || $create_superuser == "Y" ]]; then
    python manage.py createsuperuser
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your production values"
echo "2. Push your code to GitHub/GitLab"
echo "3. Deploy to your chosen platform (Railway, Heroku, etc.)"
echo "4. Set environment variables in your deployment platform"
echo "5. Test your deployed API"
echo ""
echo "For detailed instructions, see DEPLOYMENT_GUIDE.md"
echo ""
echo "🎉 Your Django Healthcare API is ready for deployment!"
