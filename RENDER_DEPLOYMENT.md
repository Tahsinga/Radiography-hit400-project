# Deployment Checklist for Render

## ✅ Pre-Deployment Checklist

### Files Created/Updated:
- [x] **Procfile** - Tells Render how to start the app
- [x] **runtime.txt** - Python version (3.11.7)
- [x] **requirements.txt** - All dependencies including dj-database-url
- [x] **settings.py** - Production settings with DATABASE_URL support
- [x] **.env.example** - Template for environment variables

### Configuration Updates:
- [x] DEBUG = False (production mode)
- [x] ALLOWED_HOSTS configured for Render
- [x] WhiteNoise middleware enabled for static files
- [x] Static files storage configured
- [x] Database config supports both SQLite (dev) and PostgreSQL (Render)
- [x] Security headers enabled for HTTPS

---

## 🚀 Deployment Steps on Render

### 1. Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create Render Account
- Go to https://render.com
- Sign up with GitHub

### 3. Create Web Service on Render
1. Click "New +" → "Web Service"
2. Select your GitHub repository
3. Configure:
   - **Name:** your-app-name
   - **Environment:** Python
   - **Region:** Choose closest to your users
   - **Build Command:**
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command:**
     ```
     gunicorn mic_radiology.wsgi:application
     ```

### 4. Add Environment Variables
In Render dashboard → Environment Variables, add:

```
SECRET_KEY=your-very-secret-key-generate-new-one
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Deploy
- Click "Create Web Service"
- Render will build and deploy automatically
- Check logs for any errors

---

## 📋 Important Notes

### Generate a New SECRET_KEY
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Database
- Render provides `DATABASE_URL` automatically when you add PostgreSQL
- Settings.py detects it and uses PostgreSQL automatically
- Initial migration runs in Build Command

### Static Files
- WhiteNoise serves static files efficiently
- CSS/JS must be collected with `collectstatic`
- Included in Build Command

### Logs
- Check Render dashboard Logs tab for errors
- Common issues:
  - Missing SECRET_KEY
  - DATABASE_URL not set
  - Static files not collected
  - Migration errors

---

## ✨ What We've Done

1. Created **Procfile** - Gunicorn start command
2. Created **runtime.txt** - Python 3.11.7
3. Updated **settings.py**:
   - Production database config with dj-database-url
   - WhiteNoise for static files
   - Security headers for HTTPS
   - DEBUG=False by default
4. Updated **requirements.txt** - Added dj-database-url
5. Security ready - SSL/TLS configured

---

## 🎯 Next Steps

1. Generate a secure SECRET_KEY
2. Push code to GitHub
3. Create web service on Render
4. Set environment variables
5. Deploy! 🚀

---

## 📞 Troubleshooting

**Build fails:**
- Check requirements.txt syntax
- Ensure all packages are compatible
- Check Python version

**App crashes after deploy:**
- Check environment variables are set
- Check SECRET_KEY is provided
- Review Render logs for errors

**Database issues:**
- Ensure DATABASE_URL is set
- Check migration errors in logs
- Verify PostgreSQL is provisioned

**Static files not loading:**
- Ensure STATIC_ROOT and STATIC_URL are correct
- WhiteNoise middleware is in MIDDLEWARE
- Run `collectstatic` locally to test

---

**Your app is now ready for production deployment on Render!** ✨
