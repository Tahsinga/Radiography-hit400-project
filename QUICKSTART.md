# QUICKSTART GUIDE

## 1. Initial Setup (Windows)

### First Time Only
```bash
# Navigate to project directory
cd HIT400_RADIOGRAPHY

# Run setup script
setup.bat

# OR manually:
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py init_data
```

### After Initial Setup
```bash
# Activate virtual environment
venv\Scripts\activate.bat

# Run development server
python manage.py runserver
```

## 2. First Time Access

- **Web Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **Login with**: Your superuser credentials created during setup

## 3. System Users & Roles

### Patient
- Can book appointments
- View appointment history
- Check payment details and shortfalls
- Download reports
- Submit feedback
- View notifications

### Radiology Staff
- Manage all appointments
- Confirm/cancel appointments
- Upload radiology reports
- Process payments
- View analytics dashboard
- Send notifications

### Referral Doctor
- View referred patients' appointments
- Access patient reports
- Track referral status

## 4. Testing the System

### Test Patient Workflow
1. Register as Patient
2. Book an appointment
3. Review payment summary
4. Receive confirmation
5. View appointment details

### Test Staff Workflow
1. Go to `/appointments/list/` to view all appointments
2. Confirm pending appointments
3. Upload reports for completed appointments
4. View analytics at `/analytics/dashboard/`

## 5. Key Features

### Appointment Booking
- **Path**: `/appointments/book/`
- Select scan type, date, time
- View payment breakdown before confirming
- Attach referral documents

### Appointment Management
- **Path**: `/appointments/list/`
- Filter by status (pending, confirmed, completed)
- Cancel appointments (24 hours notice required)
- View payment status

### Report Management
- **Path**: `/reports/{id}/upload/`
- Upload findings and PDF
- Set report status
- System auto-notifies patient

### Analytics
- **Path**: `/analytics/dashboard/`
- View KPIs and trends
- Appointment metrics
- Revenue analysis
- Patient feedback trends
- Export data

### Payment Processing
- **Path**: `/payments/{id}/process/`
- Select payment method
- Track payment status
- Handle payment shortfalls
- Insurance verification

## 6. Database Models

### Users (CustomUser)
- Standard user fields
- Role-based (patient, staff, doctor)
- Medical aid information
- Doctor license details

### Appointments
- Patient → Appointment (many-to-one)
- Scan type selection
- Date/time scheduling
- Referral document upload
- Status tracking

### Payments
- Appointment → Payment (one-to-one)
- Service charge calculation
- Medical aid coverage
- Co-payment tracking
- Payment method selection

### Reports
- Appointment → Report (one-to-one)
- Radiologist assignment
- PDF storage
- Access tracking
- Download counting

### Feedback
- Appointment → Feedback (one-to-one)
- Rating scales (1-5)
- Would recommend tracking
- Comment storage

### Notifications
- User → Notification (many-to-one)
- SMS and email channels
- Type-based templates
- Status tracking (pending, sent, delivered)

## 7. Admin Panel Features

- User management (create, edit, delete users)
- Appointment administration
- Report upload and management
- Payment processing
- Analytics access
- Notification history

## 8. Common Tasks

### Create Test Appointment
```bash
# Via web interface:
1. Login as patient
2. Go to Book Appointment
3. Select scan type
4. Choose date/time
5. Submit form
```

### Upload Report
```bash
# Via web interface:
1. Login as staff
2. Go to Appointments
3. Click appointment
4. Click Upload Report
5. Add findings, recommendations, PDF
6. Submit - patient gets notified
```

### View Analytics
```bash
# Via web interface:
1. Login as staff
2. Go to Analytics Dashboard
3. Select time range
4. View KPIs and charts
```

## 9. API Endpoints (Future Enhancement)

```
GET    /appointments/list/
POST   /appointments/book/
GET    /appointments/<id>/
POST   /appointments/<id>/cancel/
GET    /reports/<id>/view/
GET    /reports/<id>/download/
POST   /reports/<id>/feedback/
GET    /analytics/dashboard/
GET    /analytics/revenue/
GET    /analytics/feedback/
```

## 10. Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001  # Use different port
```

### Database Issues
```bash
# Fresh database
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

### Missing Templates
Ensure templates directory structure matches:
```
templates/
├── base.html
├── users/
├── appointments/
├── reports/
├── payments/
└── analytics/
```

### Static Files Issues
```bash
python manage.py collectstatic --clear --noinput
```

## 11. Configuration Files

### .env (Create from .env.example)
- SECRET_KEY (production only)
- DEBUG (True for development, False for production)
- EMAIL settings (Gmail SMTP)
- Twilio SMS settings (optional)

### settings.py
- Main Django configuration
- Database settings
- Installed apps
- Middleware
- Static files configuration

## 12. Common Django Commands

```bash
# Run development server
python manage.py runserver

# Create migrations for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create admin user
python manage.py shell
# In shell:
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@example.com', 'password123')

# Access shell
python manage.py shell

# Clear database
python manage.py flush

# Collect static files
python manage.py collectstatic

# Initialize sample data
python manage.py init_data

# Run tests
python manage.py test

# Check for issues
python manage.py check
```

## 13. Production Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Generate secure SECRET_KEY
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up email service (Gmail, SendGrid, etc.)
- [ ] Configure SMS service (Twilio)
- [ ] Set ALLOWED_HOSTS
- [ ] Enable HTTPS/SSL
- [ ] Set up Redis for Celery
- [ ] Configure static file serving (WhiteNoise)
- [ ] Set up logging
- [ ] Configure CORS if needed
- [ ] Use Gunicorn/uWSGI
- [ ] Set up reverse proxy (Nginx)
- [ ] Configure backup strategy
- [ ] Set up monitoring and alerts

## 14. Support & Resources

- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Celery Documentation: https://docs.celeryproject.org/

## 15. Next Steps

1. Complete initial setup
2. Create test accounts (patient, staff, doctor)
3. Test appointment booking workflow
4. Test report upload workflow
5. Explore analytics features
6. Configure email notifications
7. Deploy to production

---

For detailed documentation, see README.md
