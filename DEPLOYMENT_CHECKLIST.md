# ✅ Render Deployment Checklist

## Pre-Deployment Checklist

### Configuration Files
- [x] Created **Procfile**
- [x] Created **runtime.txt** (Python 3.11.7)
- [x] Updated **requirements.txt** (added dj-database-url)
- [x] Updated **settings.py** for production

### Security Setup
- [x] DEBUG set to False (production mode)
- [x] ALLOWED_HOSTS configured for Render
- [x] SECRET_KEY uses environment variable
- [x] SSL/HTTPS enforced
- [x] HSTS headers enabled
- [x] Secure cookies configured

### Database
- [x] dj-database-url installed
- [x] Database auto-detects DATABASE_URL
- [x] SQLite fallback for development
- [x] Connection pooling configured

### Static Files
- [x] WhiteNoise middleware enabled
- [x] STATIC_ROOT configured
- [x] STATICFILES_STORAGE configured (compressed)
- [x] Static directory created

### Code Validation
- [x] Django system check passes (no issues)
- [x] Server runs locally without errors
- [x] Template syntax fixed (is_authenticated)

---

## Deployment Day Checklist

### Before You Deploy

#### Step 1: Generate SECRET_KEY
```bash
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
- [ ] Generate new SECRET_KEY
- [ ] Copy the value (save somewhere safe)

#### Step 2: Code Push
```bash
git add .
git commit -m "Configure for Render deployment"
git push origin main
```
- [ ] All changes committed
- [ ] Pushed to GitHub main branch
- [ ] Verified no uncommitted changes

#### Step 3: Render Account
- [ ] Created Render account (https://render.com)
- [ ] Signed in with GitHub
- [ ] GitHub authorization completed

#### Step 4: Create Web Service
On Render Dashboard:
- [ ] Click "New +" → "Web Service"
- [ ] Selected your GitHub repository
- [ ] Service name set (e.g., "mic-radiology")
- [ ] Environment: Python ✓
- [ ] Region: Selected closest to users
- [ ] Build Command filled:
  ```
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```
- [ ] Start Command filled:
  ```
  gunicorn mic_radiology.wsgi:application
  ```

#### Step 5: Environment Variables
In Render → Environment section, add these variables:

**Required:**
- [ ] `SECRET_KEY` = (your generated key)
- [ ] `DEBUG` = `False`
- [ ] `ALLOWED_HOSTS` = `your-app-name.onrender.com,localhost`

**Security (Recommended):**
- [ ] `SECURE_SSL_REDIRECT` = `True`
- [ ] `SESSION_COOKIE_SECURE` = `True`
- [ ] `CSRF_COOKIE_SECURE` = `True`

**Email (Optional):**
- [ ] `EMAIL_BACKEND` = `django.core.mail.backends.smtp.EmailBackend`
- [ ] `EMAIL_HOST` = `smtp.gmail.com`
- [ ] `EMAIL_PORT` = `587`
- [ ] `EMAIL_USE_TLS` = `True`
- [ ] `EMAIL_HOST_USER` = (your email)
- [ ] `EMAIL_HOST_PASSWORD` = (Gmail app password)

#### Step 6: Deploy
- [ ] Review all settings one more time
- [ ] Click "Create Web Service"
- [ ] Monitor "Logs" tab during deployment
- [ ] Wait for "successfully deployed" message

---

## Post-Deployment Checklist

### Verification
- [ ] Render shows "Live" status
- [ ] App URL loads without errors
- [ ] Database migrations completed
- [ ] Static files loading (CSS/JS/images)
- [ ] No 500 errors in logs

### Testing
- [ ] Homepage loads at https://your-app.onrender.com
- [ ] Login page accessible
- [ ] CSS/JavaScript working properly
- [ ] Database queries working
- [ ] No console errors

### Monitoring
- [ ] Check Render logs daily for first week
- [ ] Monitor app performance
- [ ] Test from different browsers
- [ ] Verify HTTPS is enforced

---

## Troubleshooting Checklist

### If Deployment Fails:

#### Build Error
- [ ] Check "Logs" in Render dashboard
- [ ] Verify requirements.txt syntax
- [ ] Ensure all packages are compatible
- [ ] Check Python version (3.11.7)

#### Runtime Error
- [ ] Check SECRET_KEY is set
- [ ] Check DATABASE_URL is set
- [ ] Review Render logs for specific error
- [ ] Run `python manage.py check` locally

#### Static Files Not Loading (404)
- [ ] Verify build command includes `collectstatic`
- [ ] Check STATICFILES_STORAGE in settings
- [ ] Ensure static directory exists
- [ ] Check file permissions

#### Database Connection Error
- [ ] Verify DATABASE_URL environment variable
- [ ] Check PostgreSQL is provisioned (may need paid plan)
- [ ] Review database configuration in settings.py
- [ ] Check migration logs in Render

#### DisallowedHost Error
- [ ] Add your Render domain to ALLOWED_HOSTS
- [ ] Format: `your-app.onrender.com`
- [ ] Restart the service after updating

---

## Files You Modified/Created

### Created Files:
1. **Procfile** - Render startup instruction
2. **runtime.txt** - Python version lock
3. **RENDER_DEPLOYMENT.md** - Full deployment guide
4. **DEPLOY_INSTRUCTIONS.md** - Quick reference
5. **DEPLOYMENT_STATUS.md** - Status summary

### Modified Files:
1. **requirements.txt** - Added dj-database-url
2. **settings.py** - Production configuration

---

## Important URLs & Info

### Local Development
- URL: `http://127.0.0.1:8000`
- Database: SQLite (db.sqlite3)
- Admin: `http://127.0.0.1:8000/admin`
- Login: admin / admin123

### After Render Deployment
- URL: `https://your-app-name.onrender.com`
- Database: PostgreSQL (Render managed)
- Admin: `https://your-app-name.onrender.com/admin`
- Login: (use credentials you create)

---

## Quick Reference: Build & Start Commands

**Build Command** (Install dependencies, collect static, migrate DB):
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command** (Run the WSGI server):
```bash
gunicorn mic_radiology.wsgi:application
```

---

## Time Estimates

| Task | Time |
|------|------|
| Generate SECRET_KEY | 1 min |
| Push to GitHub | 2 min |
| Create Render account | 3 min |
| Create Web Service | 2 min |
| Set environment variables | 3 min |
| Deploy & wait | 3-5 min |
| Verify working | 2 min |
| **Total** | **~16 min** |

---

## Support Resources

- **Render Docs**: https://render.com/docs/deploy-django
- **Django Deployment**: https://docs.djangoproject.com/en/6.0/howto/deployment/
- **WhiteNoise**: https://whitenoise.readthedocs.io/
- **dj-database-url**: https://github.com/jazzband/dj-database-url

---

## ✨ Final Notes

✅ **Your app is 100% ready to deploy**

Every file is configured, every setting is optimized, and your Django app will run smoothly on Render.

**The only thing left is for YOU to:**
1. Generate SECRET_KEY
2. Push to GitHub  
3. Deploy on Render

That's it! You've got this! 🚀

---

*Checklist Date: February 4, 2026*  
*Status: ✅ READY TO DEPLOY*
