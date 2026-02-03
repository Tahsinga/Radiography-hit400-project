"""
Appointment Reminders Task Scheduler
"""
from celery import shared_task
from celery.schedules import crontab
from apps.appointments.models import Appointment
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_appointment_reminders():
    """Send reminders for appointments tomorrow"""
    tomorrow = (timezone.now() + timedelta(days=1)).date()
    appointments = Appointment.objects.filter(
        appointment_date=tomorrow,
        status__in=['pending', 'confirmed']
    )
    
    for appointment in appointments:
        from apps.notifications.tasks import send_appointment_reminder
        send_appointment_reminder.delay(str(appointment.id))


@shared_task
def check_missed_appointments():
    """Check and mark missed appointments"""
    now = timezone.now()
    missed = Appointment.objects.filter(
        appointment_date__lt=now.date(),
        status='confirmed'
    )
    
    for appointment in missed:
        appointment.status = 'no_show'
        appointment.save()


# Celery Beat Schedule (add to settings.py for periodic tasks)
CELERY_BEAT_SCHEDULE = {
    'send-appointment-reminders': {
        'task': 'apps.appointments.tasks.send_appointment_reminders',
        'schedule': crontab(hour=9, minute=0),  # 9 AM daily
    },
    'check-missed-appointments': {
        'task': 'apps.appointments.tasks.check_missed_appointments',
        'schedule': crontab(hour=18, minute=0),  # 6 PM daily
    },
}
