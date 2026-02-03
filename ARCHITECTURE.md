# System Architecture Documentation

## Overview

The MIC Radiology Management & Analytics System is a Django-based web application designed to manage radiology services with integrated e-commerce and data analytics capabilities.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                       Web Application                         │
│                  (Django Web Framework)                       │
└──────────────────────────────┬──────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
    ┌───▼────┐          ┌──────▼──────┐        ┌─────▼─────┐
    │ Users  │          │ Appointments│        │  Reports  │
    │  App   │          │     App     │        │    App    │
    └───┬────┘          └──────┬──────┘        └─────┬─────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
    ┌───▼────┐          ┌──────▼──────┐        ┌─────▼─────┐
    │Payments│          │Notifications│        │ Analytics │
    │  App   │          │     App     │        │    App    │
    └───┬────┘          └──────┬──────┘        └─────┬─────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                        ┌──────▼──────┐
                        │  Database   │
                        │  (SQLite/   │
                        │ PostgreSQL) │
                        └─────────────┘
```

## Core Apps & Their Responsibilities

### 1. Users App (`apps/users/`)
**Purpose**: User authentication, registration, and profile management

**Models**:
- `CustomUser`: Extended Django User model with role-based access

**Key Features**:
- User registration with role selection
- Profile management
- Role-based dashboards
- User authentication

**Views**:
- `register()` - User registration
- `user_login()` - Authentication
- `user_logout()` - Session termination
- `dashboard()` - Role-based redirect
- `patient_dashboard()` - Patient home
- `staff_dashboard()` - Staff home
- `doctor_dashboard()` - Doctor home
- `profile()` - Profile management

### 2. Appointments App (`apps/appointments/`)
**Purpose**: Appointment scheduling and management

**Models**:
- `Appointment` - Patient appointment records
- `ScanType` - Available radiology scans
- `MedicalAidCoverage` - Insurance information

**Key Features**:
- Online appointment booking
- Appointment confirmation workflow
- Cancellation handling (24-hour rule)
- Payment integration
- Referral tracking

**Views**:
- `book_appointment()` - New booking
- `appointment_list()` - View appointments
- `appointment_detail()` - Single appointment
- `cancel_appointment()` - Cancellation
- `edit_appointment()` - Update appointment
- `get_appointment_payment_summary()` - Payment calculation

### 3. Reports App (`apps/reports/`)
**Purpose**: Report management and patient feedback

**Models**:
- `Report` - Radiology reports
- `ReportAccess` - Access tracking
- `Feedback` - Patient feedback (in analytics)

**Key Features**:
- Report upload by radiologists
- Secure report delivery
- Download tracking
- Patient feedback collection
- Access audit trail

**Views**:
- `upload_report()` - Report creation
- `view_report()` - Report viewing
- `download_report()` - PDF download
- `submit_feedback()` - Feedback form

### 4. Payments App (`apps/payments/`)
**Purpose**: Payment processing and tracking

**Models**:
- `Payment` - Payment records
- `PaymentShortfall` - Coverage gaps

**Key Features**:
- Medical aid verification
- Payment method selection
- Shortfall identification
- Payment status tracking
- Transaction logging

**Views**:
- `process_payment()` - Payment form
- `payment_status()` - Status check
- `payment_list()` - Admin view

### 5. Notifications App (`apps/notifications/`)
**Purpose**: SMS and Email notifications

**Models**:
- `Notification` - Notification records
- `NotificationTemplate` - Reusable templates

**Key Features**:
- Email notifications
- SMS notifications (via Twilio)
- Notification templates
- Delivery tracking
- Multiple notification types

**Tasks** (Celery):
- `send_appointment_confirmation()`
- `send_appointment_reminder()`
- `send_report_ready_notification()`
- `send_payment_confirmation()`

### 6. Analytics App (`apps/analytics/`)
**Purpose**: Data analysis and business intelligence

**Models**:
- `Feedback` - Patient satisfaction data

**Key Features**:
- Appointment metrics
- Revenue analysis
- Patient satisfaction tracking
- Feedback analysis
- Trend reporting

**Views**:
- `analytics_dashboard()` - Main dashboard
- `revenue_report()` - Revenue analysis
- `feedback_analysis()` - Feedback metrics

## Database Schema

### User Model (CustomUser)
```
- id (UUID)
- username, email, password
- first_name, last_name
- phone_number, date_of_birth, gender
- address, city, postal_code
- profile_picture
- role (patient, staff, doctor)
- medical_aid_name, medical_aid_number (for patients)
- license_number, specialization (for doctors)
- is_verified, is_active, created_at, updated_at
```

### Appointment Model
```
- id (UUID)
- patient (FK: CustomUser)
- referring_doctor (FK: CustomUser, null)
- scan_type (FK: ScanType)
- appointment_date, appointment_time
- status (pending, confirmed, completed, cancelled, no_show)
- referral_document, clinical_notes
- confirmed_by (FK: CustomUser)
- reminder_sent, created_at, updated_at
```

### Payment Model
```
- id (UUID)
- appointment (OneToOne: Appointment)
- service_charge, medical_aid_coverage_amount
- patient_co_payment
- payment_method, status
- transaction_id, payment_gateway
- processed_by (FK: CustomUser)
- created_at, updated_at
```

### Report Model
```
- id (UUID)
- appointment (OneToOne: Appointment)
- radiologist (FK: CustomUser)
- status (pending, in_progress, completed, reviewed)
- findings, recommendations, pdf_file
- created_at, updated_at, completed_at
- patient_viewed_at, download_count
```

### Feedback Model
```
- id (UUID)
- appointment (OneToOne: Appointment)
- patient (FK: CustomUser)
- overall_satisfaction (1-5)
- staff_professionalism (1-5)
- facility_cleanliness (1-5)
- report_clarity (1-5)
- comments, would_recommend
- created_at
```

## User Flows

### Patient Workflow
```
1. Register → Login → Dashboard
2. Book Appointment → View Payment → Confirm
3. Receive Notifications → Arrive for Appointment
4. Upload Report Available → Download Report
5. Submit Feedback → View History
```

### Staff Workflow
```
1. Login → Dashboard
2. View Appointments → Confirm/Cancel
3. Upload Report → Send Notifications
4. Process Payments → View Analytics
```

### Doctor Workflow
```
1. Login → Dashboard
2. View Referrals → Check Status
3. View Patient Reports → Track Outcomes
```

## Key Technologies

- **Backend**: Django 4.2.8
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Task Queue**: Celery + Redis
- **Frontend**: Bootstrap 5 + JavaScript
- **APIs**: Django REST Framework
- **Analytics**: Pandas, Matplotlib, Seaborn
- **Authentication**: Django Auth + Custom User
- **File Storage**: Django FileField
- **Notifications**: Twilio SMS, Django Email

## Security Implementation

1. **Authentication**
   - User registration with validation
   - Secure password hashing
   - Session management
   - Login required decorators

2. **Authorization**
   - Role-based access control (RBAC)
   - Permission checks in views
   - Model-level filtering
   - Admin panel access control

3. **Data Protection**
   - CSRF protection
   - SQL injection prevention (ORM)
   - XSS protection (Django templates)
   - Secure file uploads
   - Report access tracking

4. **API Security**
   - Permission decorators
   - User filtering
   - Rate limiting (future)

## Scalability Considerations

1. **Database**
   - Use PostgreSQL for production
   - Add indexes on frequently queried fields
   - Implement connection pooling

2. **Caching**
   - Cache analytics results
   - Cache scan types list
   - Redis for session storage

3. **Async Tasks**
   - Use Celery for email/SMS
   - Background report processing
   - Scheduled reminders

4. **Static Files**
   - CDN for static assets
   - WhiteNoise for production

## Testing Strategy

1. **Unit Tests**
   - Model tests
   - Form validation tests
   - Utility function tests

2. **Integration Tests**
   - View tests with authentication
   - API endpoint tests
   - Database transaction tests

3. **End-to-End Tests**
   - Booking workflow
   - Payment processing
   - Report delivery

## Deployment Architecture

```
┌─────────────────┐
│   Web Browser   │
└────────┬────────┘
         │
┌────────▼────────┐
│  Load Balancer  │
└────────┬────────┘
         │
    ┌────┴─────┐
    │           │
┌───▼──┐  ┌────▼───┐
│ App1 │  │  App2  │  (Gunicorn)
└───┬──┘  └────┬───┘
    │           │
    └─────┬─────┘
          │
    ┌─────▼──────┐
    │ PostgreSQL │
    └──────┬─────┘
           │
    ┌──────▼──────┐
    │    Redis    │ (Cache & Celery)
    └─────────────┘
```

## Performance Optimization

1. **Database**
   - Query optimization (select_related, prefetch_related)
   - Database indexing
   - Connection pooling

2. **Frontend**
   - Minified CSS/JS
   - Image optimization
   - Lazy loading

3. **Backend**
   - Caching strategies
   - Async task processing
   - API pagination

## Monitoring & Logging

1. **Application Logs**
   - User authentication
   - Payment transactions
   - Error tracking

2. **System Monitoring**
   - Server health
   - Database performance
   - Task queue status

3. **Analytics**
   - User behavior
   - System usage
   - Revenue metrics

## Future Enhancements

1. **Features**
   - Mobile app (iOS/Android)
   - Video consultations
   - EHR integration
   - Insurance claim automation

2. **Technology**
   - GraphQL API
   - Real-time notifications (WebSocket)
   - Advanced analytics (ML models)
   - Microservices architecture

3. **Compliance**
   - GDPR compliance
   - HIPAA compliance
   - Data encryption at rest
   - Audit logging

---

For more details, see README.md and QUICKSTART.md
