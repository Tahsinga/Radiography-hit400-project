from celery import shared_task
from apps.notifications.models import Notification
from apps.reports.models import Report
from apps.payments.models import Payment
from django.core.mail import send_mail
from decouple import config

@shared_task
def send_appointment_confirmation(appointment_id):
    """Send appointment confirmation SMS and email"""
    from apps.appointments.models import Appointment
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        subject = f"Appointment Confirmation - {appointment.scan_type.name}"
        message = f"""
Dear {appointment.patient.first_name},

Your appointment has been scheduled for:
Date: {appointment.appointment_date}
Time: {appointment.appointment_time}
Service: {appointment.scan_type.name}

Please arrive 15 minutes early.

Best regards,
MIC Radiology Management System
        """
        
        # Create notification records
        Notification.objects.create(
            recipient=appointment.patient,
            notification_type='appointment_confirmation',
            channel='both',
            subject=subject,
            message=message,
            appointment=appointment,
            status='sent'
        )
        
        # Send email
        try:
            from_email = config('EMAIL_HOST_USER', default='noreply@micradiology.com')
            if isinstance(from_email, str):
                send_mail(
                    subject,
                    message,
                    from_email,
                    [appointment.patient.email],
                    fail_silently=True,
                )
        except:
            pass
        
        # Send SMS (integrate with Twilio)
        # send_sms_notification(appointment.patient.phone_number, message[:160])
        
    except Appointment.DoesNotExist:
        pass


@shared_task
def send_appointment_reminder(appointment_id):
    """Send appointment reminder"""
    from apps.appointments.models import Appointment
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        if appointment.reminder_sent:
            return
        
        subject = "Appointment Reminder"
        message = f"""
Dear {appointment.patient.first_name},

This is a reminder about your upcoming appointment:
Date: {appointment.appointment_date}
Time: {appointment.appointment_time}
Service: {appointment.scan_type.name}

Please call +1-234-567 to reschedule if needed.

Best regards,
MIC Radiology Management System
        """
        
        Notification.objects.create(
            recipient=appointment.patient,
            notification_type='appointment_reminder',
            channel='both',
            subject=subject,
            message=message,
            appointment=appointment,
            status='sent'
        )
        
        appointment.reminder_sent = True
        appointment.save()
        
    except Appointment.DoesNotExist:
        pass


@shared_task
def send_report_ready_notification(report_id):
    """Notify patient that report is ready"""
    try:
        report = Report.objects.get(id=report_id)
        appointment = report.appointment
        
        subject = "Your Radiology Report is Ready"
        message = f"""
Dear {appointment.patient.first_name},

Your radiology report for {appointment.scan_type.name} is now ready for download.

Log in to your account to view and download your report.

Best regards,
MIC Radiology Management System
        """
        
        Notification.objects.create(
            recipient=appointment.patient,
            notification_type='report_ready',
            channel='both',
            subject=subject,
            message=message,
            appointment=appointment,
            status='sent'
        )
        
        # Also notify referring doctor if available
        if appointment.referring_doctor:
            Notification.objects.create(
                recipient=appointment.referring_doctor,
                notification_type='report_ready',
                channel='email',
                subject=subject,
                message=message,
                appointment=appointment,
                status='sent'
            )
        
    except Report.DoesNotExist:
        pass


@shared_task
def send_payment_confirmation(payment_id):  # type: ignore
    """Send payment confirmation"""
    try:
        payment = Payment.objects.get(id=payment_id)
        appointment = payment.appointment
        
        subject = "Payment Received"
        payment_status = payment.get_status_display()  # type: ignore
        message = f"""
Dear {appointment.patient.first_name},

We have received your payment of {payment.service_charge}.

Transaction ID: {payment.transaction_id or payment.id}
Status: {payment_status}

Your appointment is confirmed for {appointment.appointment_date} at {appointment.appointment_time}.

Best regards,
MIC Radiology Management System
        """
        
        Notification.objects.create(
            recipient=appointment.patient,
            notification_type='appointment_confirmation',
            channel='both',
            subject=subject,
            message=message,
            appointment=appointment,
            status='sent'
        )
        
    except Payment.DoesNotExist:
        pass
