# 🚀 Django Healthcare API Deployment Guide

This guide will help you deploy your Django Healthcare Management API to various cloud platforms.

## 📋 Prerequisites

1. **Git repository** - Your code should be in a Git repository (GitHub, GitLab, etc.)
2. **Database** - Production database (PostgreSQL recommended)
3. **Environment variables** - Set up using `.env` file

## 🚀 Deployment Options

### Option 1: Railway (Recommended - Easiest)

Railway is perfect for Django applications and offers a generous free tier.

#### Steps:
1. **Sign up**: Go to [railway.app](https://railway.app) and sign up with GitHub
2. **Create new project**: Click "New Project" → "Deploy from GitHub repo"
3. **Select repository**: Choose your Django project repository
4. **Environment variables**: Add these variables in Railway dashboard:
   ```
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app
   DJANGO_SETTINGS_MODULE=APIs.settings_prod
   ```
5. **Database**: Railway will automatically provision PostgreSQL
6. **Deploy**: Railway will automatically build and deploy your app

#### Custom Domain (Optional):
- Go to Settings → Domains
- Add your custom domain
- Update `ALLOWED_HOSTS` in environment variables

---

### Option 2: Heroku

Classic platform with excellent Django support.

#### Steps:
1. **Install Heroku CLI**: Download from [heroku.com](https://heroku.com)
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-app-name`
4. **Environment variables**:
   ```bash
   heroku config:set SECRET_KEY=your-super-secret-key-here
   heroku config:set DEBUG=False
   heroku config:set DJANGO_SETTINGS_MODULE=APIs.settings_prod
   ```
5. **Database**: `heroku addons:create heroku-postgresql:hobby-dev`
6. **Deploy**: 
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push heroku main
   ```

---

### Option 3: DigitalOcean App Platform

Great balance of simplicity and power.

#### Steps:
1. **Sign up**: Create account at [digitalocean.com](https://digitalocean.com)
2. **Create app**: Go to Apps → Create App
3. **Connect GitHub**: Select your repository
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn APIs.wsgi:application`
5. **Environment variables**: Add all required variables
6. **Database**: Add PostgreSQL database component
7. **Deploy**: Click "Create Resources"

---

### Option 4: AWS Elastic Beanstalk

Enterprise-grade deployment with AWS services.

#### Steps:
1. **Install EB CLI**: `pip install awsebcli`
2. **Initialize**: `eb init`
3. **Create environment**: `eb create production`
4. **Configure**: Update environment variables in AWS console
5. **Deploy**: `eb deploy`

---

## 🔧 Pre-Deployment Checklist

### 1. Update Settings
- ✅ Created `settings_prod.py` with production settings
- ✅ Added `whitenoise` for static file serving
- ✅ Configured database with `dj-database-url`
- ✅ Added security headers for production

### 2. Dependencies
- ✅ Updated `requirements.txt` with production packages
- ✅ Added `gunicorn` for WSGI server
- ✅ Added `psycopg2-binary` for PostgreSQL

### 3. Process Files
- ✅ Created `Procfile` for process management
- ✅ Created `runtime.txt` with Python version
- ✅ Created `.gitignore` to exclude sensitive files

### 4. Environment Setup
- ✅ Created `.env.example` with required variables
- ✅ Added configuration for environment variables

## 🔐 Environment Variables You Need

Create these environment variables in your deployment platform:

```env
# Required
SECRET_KEY=your-super-secret-django-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://username:password@hostname:port/database_name

# Optional
OPENAI_API_KEY=your-openai-api-key
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

## 🗄️ Database Migration

After deployment, run these commands to set up your database:

```bash
# For Railway/Heroku (automatically runs)
python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser (run once)
python manage.py createsuperuser
```

## 🚦 Testing Your Deployment

1. **Health Check**: `GET https://your-app-url.com/health/`
2. **API Documentation**: `GET https://your-app-url.com/`
3. **Login**: `POST https://your-app-url.com/api/v1/auth/login/`

## 📊 Monitoring & Maintenance

### Log Monitoring
- **Railway**: View logs in Railway dashboard
- **Heroku**: `heroku logs --tail`
- **DigitalOcean**: Check runtime logs in console

### Database Backup
- Set up automated backups in your platform
- Export data periodically for safety

### Updates
- Push code changes to Git
- Platform will automatically redeploy

## 💡 Tips for Success

1. **Start with Railway** - Easiest to get started
2. **Use PostgreSQL** - Much better than SQLite for production
3. **Set up monitoring** - Use platform monitoring tools
4. **Test thoroughly** - Test all endpoints after deployment
5. **Secure your API** - Use HTTPS and proper authentication

## 🚨 Common Issues & Solutions

### Issue: Static files not loading
**Solution**: Ensure `whitenoise` is installed and configured

### Issue: Database connection errors
**Solution**: Check `DATABASE_URL` format and credentials

### Issue: CORS errors
**Solution**: Add your frontend domain to `CORS_ALLOWED_ORIGINS`

### Issue: Secret key errors
**Solution**: Generate a new secret key and add to environment variables

## 🎯 Next Steps

1. Choose your preferred deployment platform
2. Set up environment variables
3. Connect your Git repository
4. Deploy and test
5. Set up custom domain (optional)
6. Monitor and maintain

Your Django Healthcare API is now ready for production deployment! 🎉

---

## 📞 Support

If you need help with deployment:
1. Check platform documentation
2. Review deployment logs
3. Test locally first
4. Verify all environment variables are set correctly

Good luck with your deployment! 🚀
