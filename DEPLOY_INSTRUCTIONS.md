# 🚀 Render Deployment Guide for MIC Radiology

## Summary of Changes Made

### Files Created:
1. ✅ **Procfile** - Instructs Render how to start the app
2. ✅ **runtime.txt** - Specifies Python 3.11.7
3. ✅ **RENDER_DEPLOYMENT.md** - Complete deployment instructions

### Files Updated:
1. ✅ **requirements.txt** - Added `dj-database-url==2.1.0`
2. ✅ **settings.py** - Production-ready configuration

---

## What Was Changed in settings.py

### 1. Imports
```python
import dj_database_url  # NEW - For Render DATABASE_URL
```

### 2. DEBUG Mode
```python
# Changed from: DEBUG = config('DEBUG', default=True, cast=bool)
DEBUG = config('DEBUG', default=False, cast=bool)  # Production mode
```

### 3. Database Configuration
```python
# Supports both PostgreSQL (Render) and SQLite (development)
if config('DATABASE_URL', default=''):
    # Production: Render provides DATABASE_URL
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Development: Uses SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### 4. Static Files for Production
```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```
*(WhiteNoise is already in MIDDLEWARE)*

### 5. Security Headers
```python
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool) if not DEBUG else False
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool) if not DEBUG else False
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool) if not DEBUG else False
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
```

---

## Procfile Content
```
web: gunicorn mic_radiology.wsgi:application
```

---

## ✨ Your App is Ready to Deploy!

### Next Steps:

#### Step 1: Generate a Secure SECRET_KEY
Run in Python shell:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
# Copy the output
```

#### Step 2: Push to GitHub
```bash
git add .
git commit -m "Configure for Render deployment"
git push origin main
```

#### Step 3: Create Render Account
Go to https://render.com and sign up with GitHub.

#### Step 4: Create Web Service
1. Click "New +" → "Web Service"
2. Select your GitHub repository
3. Configure:
   - **Name**: (your-app-name)
   - **Environment**: Python
   - **Region**: Closest to you
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**: 
     ```
     gunicorn mic_radiology.wsgi:application
     ```

#### Step 5: Set Environment Variables
In Render Dashboard → Environment:

| Variable | Value | Notes |
|----------|-------|-------|
| `SECRET_KEY` | (your generated key) | Critical - keep secure |
| `DEBUG` | `False` | Production mode |
| `ALLOWED_HOSTS` | `your-app.onrender.com,localhost` | Update with your domain |
| `SECURE_SSL_REDIRECT` | `True` | Enable HTTPS |
| `SESSION_COOKIE_SECURE` | `True` | Secure cookies |
| `CSRF_COOKIE_SECURE` | `True` | Secure CSRF |

**Optional Email Setup** (for notifications):
| Variable | Value |
|----------|-------|
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `True` |
| `EMAIL_HOST_USER` | (your email) |
| `EMAIL_HOST_PASSWORD` | (Gmail app password) |

#### Step 6: Deploy
1. Click "Create Web Service"
2. Render builds and deploys automatically
3. Check "Logs" tab for progress

---

## 📊 Deployment Architecture

```
Local Development:
├── SQLite (db.sqlite3)
├── DEBUG = True
└── Static files served by Django

Production on Render:
├── PostgreSQL (provided by Render)
├── DEBUG = False
├── WhiteNoise serves static files (compressed)
├── Gunicorn WSGI server
└── SSL/HTTPS enforced
```

---

## ✅ What's Configured

### Security ✨
- ✅ SSL/HTTPS enforced
- ✅ Secure cookies (HTTP only, secure flag)
- ✅ CSRF protection
- ✅ HSTS headers
- ✅ WhiteNoise for efficient static file serving

### Database 🗄️
- ✅ Auto-detects DATABASE_URL (Render PostgreSQL)
- ✅ Falls back to SQLite for local development
- ✅ Connection pooling configured
- ✅ Health checks enabled

### Performance 🚀
- ✅ Gunicorn WSGI server
- ✅ Static files compressed (WhiteNoise)
- ✅ Database connection pooling
- ✅ Proper caching headers

### Deployment 📦
- ✅ Procfile for Render startup
- ✅ Python version locked to 3.11.7
- ✅ Requirements.txt complete
- ✅ Build migrations automated

---

## 🐛 Common Issues & Solutions

### "ModuleNotFoundError: No module named 'dj_database_url'"
**Fix**: `pip install -r requirements.txt` (already updated)

### "DisallowedHost at /..."
**Fix**: Add your Render domain to ALLOWED_HOSTS environment variable
```
your-app.onrender.com
```

### "Static files not loading (404)"
**Fix**: Ensure build command includes `collectstatic`
```
python manage.py collectstatic --noinput
```

### "Database connection error"
**Fix**: Check DATABASE_URL environment variable is set in Render dashboard

### "Secret key error"
**Fix**: Generate a new SECRET_KEY and set it in environment variables

---

## 🔧 Local Development (after deployment setup)

To test production settings locally:
```bash
# Set environment variables in .env file
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Then run:
python manage.py runserver
```

---

## 📚 Resources

- [Render Django Docs](https://render.com/docs/deploy-django)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
- [WhiteNoise Docs](https://whitenoise.readthedocs.io/)
- [dj-database-url](https://github.com/jazzband/dj-database-url)

---

## ✨ You're All Set!

Your MIC Radiology application is now configured for production deployment on Render. 

**Total setup time**: ~5 minutes on Render

**Questions?** Check the logs in Render Dashboard → Logs tab for any errors.

Good luck! 🚀
