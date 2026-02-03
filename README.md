# MIC Radiology Management & Analytics System

A comprehensive Django web application for managing radiology services with e-commerce and data science analytics capabilities.

## Features

### E-Commerce Features
- **Online Appointment Booking**: Patients can book radiology services online with real-time availability
- **Payment Transparency**: Display medical aid coverage, shortfalls, and co-payments before appointment
- **Digital Referral Submission**: Patients can upload referral documents digitally
- **Secure Report Delivery**: Patients access reports securely with download tracking
- **Feedback Collection**: Post-appointment feedback and satisfaction ratings

### Data Science & Analytics
- **Appointment Analytics**: Track appointments by day, week, month
- **Revenue Analysis**: Revenue trends, scan type breakdown, payment method analysis
- **Missed Appointment Tracking**: Identify patterns and trends
- **Patient Satisfaction Metrics**: Feedback analysis and recommendations tracking
- **Staff Performance Metrics**: Track radiologist turnaround times
- **Predictive Analytics**: Identify high-risk missed appointments

### Core Functionality
- **Role-Based Access Control**: 
  - Patients: Book appointments, view reports, submit feedback
  - Staff/Admin: Manage appointments, upload reports, view analytics
  - Referral Doctors: Track referrals, view patient reports
- **Automated Notifications**: SMS and email reminders (appointment confirmation, reminders, report ready)
- **Medical Aid Integration**: Track coverage and patient co-payments
- **Report Management**: Secure upload, storage, and download with access tracking
- **User Management**: Registration, profile management, role assignment

## Tech Stack

- **Backend**: Django 4.2.8
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Bootstrap 5, jQuery
- **Task Queue**: Celery + Redis (for notifications)
- **Analytics**: Pandas, Matplotlib, Seaborn
- **API**: Django REST Framework
- **Authentication**: Django built-in + Custom User Model

## Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)
- Redis (for Celery tasks)

### Setup Steps

1. **Clone the repository**
```bash
cd HIT400_RADIOGRAPHY
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```bash
copy .env.example .env
```

5. **Update .env with your settings**
```
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
```

6. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```

8. **Load initial data (optional)**
```bash
python manage.py loaddata initial_scantypes.json
```

9. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

10. **Run development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## Usage

### User Registration & Login
- Navigate to `/register/` to create an account (Patient, Referral Doctor, or Staff)
- Login at `/login/`

### Patient Features
- **Book Appointment**: Navigate to "Book Appointment" and select scan type, date, time
- **View Payment Details**: See medical aid coverage and co-payment before booking
- **Download Reports**: Access completed reports securely
- **Submit Feedback**: Rate your experience after appointment completion

### Staff Features
- **Manage Appointments**: View, confirm, edit, or cancel appointments
- **Upload Reports**: Add findings, recommendations, and PDF reports
- **Send Notifications**: Automated SMS/email for confirmations and reminders
- **Analytics Dashboard**: View key metrics and trends
- **Revenue Reports**: Analyze revenue by scan type and payment method
- **Patient Feedback**: Review satisfaction metrics and recommendations

### Analytics & Reporting
- **Dashboard**: Overview of key metrics (appointments, revenue, satisfaction)
- **Revenue Report**: Detailed revenue analysis and trends
- **Feedback Analysis**: Patient satisfaction trends and breakdowns

## Project Structure

```
HIT400_RADIOGRAPHY/
├── mic_radiology/           # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/               # User management & authentication
│   ├── appointments/        # Appointment booking & management
│   ├── reports/             # Report management & feedback
│   ├── payments/            # Payment processing & tracking
│   ├── analytics/           # Analytics & dashboards
│   └── notifications/       # SMS & Email notifications
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── manage.py
└── requirements.txt
```

## API Endpoints

### Users
- `POST /register/` - User registration
- `POST /login/` - User login
- `POST /logout/` - User logout
- `GET /profile/` - User profile
- `GET /dashboard/` - Role-based dashboard

### Appointments
- `GET /appointments/list/` - List appointments
- `POST /appointments/book/` - Book appointment
- `GET /appointments/<id>/` - Appointment details
- `POST /appointments/<id>/cancel/` - Cancel appointment
- `GET /appointments/<id>/payment-summary/` - Payment calculation

### Reports
- `POST /reports/<id>/upload/` - Upload report
- `GET /reports/<id>/view/` - View report
- `GET /reports/<id>/download/` - Download report PDF
- `POST /reports/<id>/feedback/` - Submit feedback

### Analytics
- `GET /analytics/dashboard/` - Analytics dashboard
- `GET /analytics/revenue/` - Revenue analysis
- `GET /analytics/feedback/` - Feedback analysis

## Configuration

### Email Settings
Update `.env` with your email provider:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### SMS Notifications (Twilio)
Configure Twilio credentials in `.env`:
```
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890
```

### Database Configuration
For PostgreSQL:
```
DATABASE_URL=postgresql://user:password@localhost:5432/mic_radiology
```

## Development

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Running Tests
```bash
python manage.py test
```

### Creating Admin User
```bash
python manage.py createsuperuser
```

### Admin Panel
Access Django admin at `/admin/` with superuser credentials

## Deployment

### Production Checklist
1. Set `DEBUG=False` in production
2. Update `SECRET_KEY` to a secure random value
3. Set `ALLOWED_HOSTS` to your domain
4. Configure database (PostgreSQL recommended)
5. Set up SSL/HTTPS
6. Configure email service
7. Set up Redis for Celery
8. Use Gunicorn or uWSGI as WSGI server
9. Configure reverse proxy (Nginx/Apache)
10. Set up static file serving

### Using Gunicorn
```bash
gunicorn mic_radiology.wsgi:application --bind 0.0.0.0:8000
```

## Troubleshooting

### Database Migration Issues
```bash
python manage.py migrate --fake users zero
python manage.py migrate users
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Template Not Found
Ensure `TEMPLATES` setting in `settings.py` points to correct directory

## Support

For issues and questions:
1. Check logs: `python manage.py runserver`
2. Review Django documentation: https://docs.djangoproject.com/
3. Check app-specific README files

## License

MIC Radiology Management System - 2024

## Contributors

- Development Team

## Future Enhancements

- Mobile app (iOS/Android) development
- Integration with EHR systems
- Advanced predictive analytics
- Machine learning for appointment no-show prediction
- Real-time appointment scheduling with calendar sync
- Video consultation integration
- Insurance claim automation
