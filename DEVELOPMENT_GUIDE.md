# Development Guide - MIC Radiology Management System

## For Developers

### Setting Up Development Environment

#### Prerequisites
- Python 3.8+
- pip
- Git
- Virtual environment manager (venv or virtualenv)

#### Step-by-Step Setup

1. **Clone & Navigate**
```bash
cd HIT400_RADIOGRAPHY
```

2. **Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
# Copy example to .env
copy .env.example .env  # Windows
cp .env.example .env   # Linux/Mac

# Edit .env with your settings
# Minimum required:
# SECRET_KEY=your-secret-key
# DEBUG=True
```

5. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py init_data
```

6. **Create Test Users**
```bash
# Create superuser
python manage.py createsuperuser

# Or use shell to create additional users
python manage.py shell
# In shell:
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.create_user(
    username='testpatient',
    email='patient@example.com',
    password='password123',
    role='patient'
)
```

7. **Run Development Server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000`

### Project Structure Understanding

#### Key Directories
```
/mic_radiology      - Main project configuration
/apps              - All Django applications
/templates         - HTML templates
/static            - CSS, JS, images (when collected)
/media             - User uploads (reports, documents)
```

#### App Organization Pattern
Each app follows this structure:
```
app_name/
├── migrations/     - Database migrations
├── templates/      - App-specific templates
├── __init__.py
├── admin.py        - Admin panel configuration
├── apps.py         - App configuration
├── forms.py        - Form definitions
├── models.py       - Data models
├── tests.py        - Unit tests
├── urls.py         - URL routing
├── views.py        - View logic
├── tasks.py        - Celery tasks (if async needed)
└── management/     - Management commands
```

### Making Code Changes

#### Adding a New Feature

1. **Define the Model**
```python
# In relevant app/models.py
from django.db import models

class NewModel(models.Model):
    name = models.CharField(max_length=100)
    # ... other fields
    
    def __str__(self):
        return self.name
```

2. **Create Migration**
```bash
python manage.py makemigrations app_name
python manage.py migrate
```

3. **Register in Admin**
```python
# In app/admin.py
from django.contrib import admin
from .models import NewModel

@admin.register(NewModel)
class NewModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
```

4. **Create Form**
```python
# In app/forms.py
from django import forms
from .models import NewModel

class NewModelForm(forms.ModelForm):
    class Meta:
        model = NewModel
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
```

5. **Create View**
```python
# In app/views.py
from django.shortcuts import render
from .models import NewModel
from .forms import NewModelForm

def new_model_list(request):
    objects = NewModel.objects.all()
    return render(request, 'app_name/list.html', {'objects': objects})
```

6. **Create Template**
```html
<!-- In templates/app_name/list.html -->
{% extends 'base.html' %}

{% block content %}
<h2>List</h2>
{% for obj in objects %}
    <p>{{ obj.name }}</p>
{% endfor %}
{% endblock %}
```

7. **Add URL Route**
```python
# In app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.new_model_list, name='new_model_list'),
]
```

### Common Development Tasks

#### Running Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test apps.users

# With verbosity
python manage.py test -v 2
```

#### Creating a Custom Management Command
```python
# Create: app/management/commands/my_command.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'My custom command'
    
    def handle(self, *args, **options):
        self.stdout.write('Command executed!')
```

Run with:
```bash
python manage.py my_command
```

#### Database Operations

```bash
# Reset database (caution!)
python manage.py flush

# Check migrations
python manage.py showmigrations

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create SQL
python manage.py sqlmigrate app_name migration_number
```

#### Shell Access
```bash
python manage.py shell

# Now you can:
from apps.users.models import CustomUser
users = CustomUser.objects.all()
user = CustomUser.objects.get(username='testuser')
```

#### Creating Fixtures (Test Data)
```bash
# Export data
python manage.py dumpdata apps.appointments > apps/appointments/fixtures/sample_data.json

# Import data
python manage.py loaddata apps/appointments/fixtures/sample_data.json
```

### Debugging

#### Print Debugging
```python
# In views or models
print("Debug message:", variable)
# Then check console output
```

#### Django Debug Toolbar (Optional)
```bash
pip install django-debug-toolbar
```

Add to INSTALLED_APPS in settings.py

#### Logging
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Info message")
logger.error("Error occurred")
```

### Code Quality

#### Style Guide (PEP 8)
```bash
# Install linter
pip install flake8

# Check code
flake8 .
```

#### Format Code
```bash
pip install black
black .
```

### Database Queries Best Practices

#### Efficient Queries
```python
# ❌ Bad - N+1 Query Problem
appointments = Appointment.objects.all()
for apt in appointments:
    patient = apt.patient  # Query each time

# ✅ Good - Use select_related
appointments = Appointment.objects.select_related('patient')
for apt in appointments:
    patient = apt.patient  # No extra query
```

#### Query Optimization
```python
# Use only needed fields
Appointment.objects.values_list('id', 'status')

# Filter early
Appointment.objects.filter(status='completed').count()

# Use exists() for existence checks
if Appointment.objects.filter(id=1).exists():
    pass
```

### Celery & Background Tasks

#### Creating a Task
```python
# In app/tasks.py
from celery import shared_task

@shared_task
def send_email_task(email, subject):
    # Send email
    pass
```

#### Calling a Task
```python
# Async call
send_email_task.delay(email, subject)

# Scheduled
from celery import current_app
current_app.send_task('app.tasks.send_email_task', args=[email, subject])
```

#### Running Celery
```bash
# Terminal 1: Start Celery worker
celery -A mic_radiology worker -l info

# Terminal 2: Start Celery beat (scheduler)
celery -A mic_radiology beat -l info

# In same terminal (development)
celery -A mic_radiology worker -l info --beat
```

### Testing Examples

#### Model Test
```python
# In app/tests.py
from django.test import TestCase
from .models import MyModel

class MyModelTest(TestCase):
    def setUp(self):
        MyModel.objects.create(name='Test')
    
    def test_model_creation(self):
        obj = MyModel.objects.get(name='Test')
        self.assertEqual(obj.name, 'Test')
```

#### View Test
```python
from django.test import Client, TestCase
from django.urls import reverse

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_view_access(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
```

### Version Control

#### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
git add .

# Commit changes
git commit -m "Add new feature description"

# Push to remote
git push origin feature/new-feature

# Create pull request
```

#### .gitignore
```
venv/
*.pyc
__pycache__/
.env
db.sqlite3
/media/
/staticfiles/
.DS_Store
*.log
.idea/
.vscode/
```

### Performance Optimization

#### Caching
```python
from django.core.cache import cache

# Set cache
cache.set('key', value, 3600)  # 1 hour

# Get cache
value = cache.get('key')

# Delete cache
cache.delete('key')
```

#### Query Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def expensive_view(request):
    pass
```

### Deployment Preparation

#### Pre-deployment Checklist
- [ ] `DEBUG = False` in settings
- [ ] `SECRET_KEY` updated
- [ ] `ALLOWED_HOSTS` configured
- [ ] Database migrations run
- [ ] Static files collected
- [ ] Environment variables set
- [ ] Email configured
- [ ] Logs configured
- [ ] Backups configured
- [ ] HTTPS enabled

#### Creating Requirements from Installed Packages
```bash
pip freeze > requirements.txt
```

### Useful Links & Resources

- Django Docs: https://docs.djangoproject.com/
- Python PEP 8: https://pep8.org/
- Git Documentation: https://git-scm.com/doc
- Bootstrap Docs: https://getbootstrap.com/docs/
- Celery Docs: https://docs.celeryproject.org/

### File Organization Best Practices

```python
# Good file organization:
# - Keep models.py focused on models only
# - Keep views.py focused on view logic
# - Create separate files for complex logic
#   - services.py (business logic)
#   - utils.py (utility functions)
#   - signals.py (Django signals)
#   - serializers.py (DRF serializers)
```

### Troubleshooting Common Issues

#### ModuleNotFoundError
```bash
# Ensure app is in INSTALLED_APPS
# Ensure __init__.py exists in all directories
```

#### Template Not Found
```bash
# Check TEMPLATES setting in settings.py
# Ensure template path is correct
# Ensure app is in INSTALLED_APPS
```

#### Database Error
```bash
# Delete migrations (if safe)
# Run: python manage.py makemigrations
# Run: python manage.py migrate
```

#### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

---

Happy coding! For more help, refer to README.md and official Django documentation.
