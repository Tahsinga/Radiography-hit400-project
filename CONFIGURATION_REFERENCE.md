# MIC Radiology System - Configuration Reference

## Environment Variables (.env)

Create a `.env` file in the project root by copying `.env.example`:

```bash
cp .env.example .env
```

### Django Core Settings

```env
# SECRET_KEY - Keep this secret and unique
# Generate: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY=your-secret-key-here

# DEBUG mode - Set to False in production
DEBUG=True

# Allowed hosts for production deployment
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

### Database Configuration

#### Development (SQLite)
```env
# Default SQLite configuration
DATABASE_URL=sqlite:///db.sqlite3
```

#### Production (PostgreSQL)
```env
# PostgreSQL connection
DATABASE_URL=postgresql://username:password@localhost:5432/mic_radiology_db

# Example:
DATABASE_URL=postgresql://admin:securepass@db.example.com:5432/radiology
```

### Email Configuration

#### Console Backend (Development)
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

#### Gmail SMTP
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
```

#### SendGrid
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.your-sendgrid-api-key
```

#### AWS SES
```env
EMAIL_BACKEND=django_ses.SESBackend
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_SES_REGION_NAME=us-east-1
AWS_SES_REGION_ENDPOINT=email.us-east-1.amazonaws.com
```

### SMS Configuration (Twilio)

```env
# Twilio Account Settings
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# Example:
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+1234567890
```

### Celery Configuration (Background Tasks)

```env
# Redis URL for Celery Broker
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379

# Production Example:
CELERY_BROKER_URL=redis://redis-server:6379/0
CELERY_RESULT_BACKEND=redis://redis-server:6379/1
```

### Security Settings

```env
# HTTPS/SSL Settings (Production)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# Production settings:
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# HSTS Header
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

---

## Settings.py Configuration

### Key Settings in `mic_radiology/settings.py`

#### Installed Apps
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
    
    # Local apps
    'apps.users',
    'apps.appointments',
    'apps.reports',
    'apps.payments',
    'apps.analytics',
    'apps.notifications',
]
```

#### Middleware
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

#### Database
```python
# Development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Production PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mic_radiology',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }
}
```

#### Static Files
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Production with WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### Media Files
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

#### Templates
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

#### Authentication
```python
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
SESSION_COOKIE_AGE = 86400  # 24 hours
```

#### REST Framework
```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

#### Crispy Forms
```python
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

---

## Running the Application

### Development Server
```bash
python manage.py runserver
# Accessible at http://localhost:8000
```

### With Custom Port
```bash
python manage.py runserver 8080
```

### Celery Workers (for notifications)
```bash
# Terminal 1: Celery Worker
celery -A mic_radiology worker -l info

# Terminal 2: Celery Beat (scheduler)
celery -A mic_radiology beat -l info

# Or combined (development only):
celery -A mic_radiology worker -l info --beat
```

---

## Common Commands

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Flush database (⚠️ deletes all data)
python manage.py flush

# Create superuser
python manage.py createsuperuser

# Initialize sample data
python manage.py init_data
```

### Static Files
```bash
# Collect static files (production)
python manage.py collectstatic --noinput

# Collect and remove old files
python manage.py collectstatic --clear --noinput
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.users

# With verbosity
python manage.py test -v 2
```

### Shell Access
```bash
python manage.py shell

# Inside shell:
from apps.users.models import CustomUser
from apps.appointments.models import Appointment
users = CustomUser.objects.all()
```

---

## Production Deployment Checklist

### Before Deployment
- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` is secure and unique
- [ ] `ALLOWED_HOSTS` is configured
- [ ] Database is PostgreSQL
- [ ] Redis is running
- [ ] Email service configured
- [ ] SMS service configured (optional)
- [ ] Static files collected
- [ ] HTTPS/SSL configured
- [ ] Backups configured
- [ ] Logging configured
- [ ] Monitoring setup

### Using Gunicorn
```bash
# Installation
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:8000 mic_radiology.wsgi:application

# With configuration file
gunicorn -c gunicorn_config.py mic_radiology.wsgi:application
```

### Systemd Service (Linux)
```ini
# /etc/systemd/system/mic-radiology.service
[Unit]
Description=MIC Radiology Service
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/user/HIT400_RADIOGRAPHY
ExecStart=/home/user/HIT400_RADIOGRAPHY/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/run/mic-radiology.sock \
    mic_radiology.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /home/user/HIT400_RADIOGRAPHY/staticfiles/;
    }

    location /media/ {
        alias /home/user/HIT400_RADIOGRAPHY/media/;
    }

    location / {
        proxy_pass http://unix:/run/mic-radiology.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Troubleshooting

### Common Issues

#### ModuleNotFoundError
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt
```

#### Database Migration Issues
```bash
# Reset migrations (caution!)
python manage.py migrate apps.users zero
python manage.py migrate apps.users
```

#### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
# In development, ensure DEBUG=True
```

#### Template Not Found
- Check TEMPLATES setting
- Ensure app is in INSTALLED_APPS
- Verify template directory structure

#### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001

# Or find and kill process
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -i :8000
```

---

## Performance Tuning

### Database Optimization
```python
# Use select_related for ForeignKey
appointments = Appointment.objects.select_related('patient')

# Use prefetch_related for reverse relations
patients = CustomUser.objects.prefetch_related('appointments')

# Add database indexes
class Meta:
    indexes = [
        models.Index(fields=['user', 'status']),
    ]
```

### Caching
```python
from django.core.cache import cache

# Cache for 1 hour
cache.set('key', value, 3600)

# Cache template fragment
{% load cache %}
{% cache 3600 my_cache %}
    expensive_content
{% endcache %}
```

### Query Optimization
```python
# Count efficiently
count = Model.objects.filter(status='active').count()

# Check existence
if Model.objects.filter(id=1).exists():
    pass
```

---

## Monitoring & Logging

### Django Logging Configuration
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Accessing Logs
```bash
# View logs in real-time
tail -f logs/debug.log

# Search logs
grep "ERROR" logs/debug.log
```

---

## Backup & Recovery

### Database Backup (PostgreSQL)
```bash
# Backup
pg_dump mic_radiology > backup.sql

# Restore
psql mic_radiology < backup.sql
```

### Media Files Backup
```bash
# Backup media files
tar -czf media_backup.tar.gz media/

# Restore
tar -xzf media_backup.tar.gz
```

---

## Additional Resources

- Settings Documentation: https://docs.djangoproject.com/en/4.2/ref/settings/
- Email Backend: https://docs.djangoproject.com/en/4.2/topics/email/
- Celery: https://docs.celeryproject.org/
- Gunicorn: https://gunicorn.org/
- Nginx: https://nginx.org/

---

**Last Updated**: January 2026
**For more help**: See README.md, QUICKSTART.md, ARCHITECTURE.md
