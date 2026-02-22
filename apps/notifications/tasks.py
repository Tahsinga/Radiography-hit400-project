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
def send_appointment_completed(appointment_id, completed_by_id=None):
    """Notify patient, referring doctor and receptionist that an appointment was completed."""
    from apps.appointments.models import Appointment
    from apps.users.models import CustomUser
    from django.core.mail import send_mail
    from decouple import config
    try:
        appointment = Appointment.objects.get(id=appointment_id)

        completed_by = None
        if completed_by_id:
            try:
                completed_by = CustomUser.objects.get(id=completed_by_id)
            except Exception:
                completed_by = None

        subject = f"Appointment Completed - {appointment.scan_type.name if appointment.scan_type else 'Appointment'}"
        patient_message = f"""
Dear {appointment.patient.first_name},

Your appointment scheduled for {appointment.appointment_date} at {appointment.appointment_time} has been marked as completed.
Marked completed by: {completed_by.get_full_name() if completed_by else 'System'}.

You can log in to view any reports or follow-up instructions.

Best regards,
MIC Radiology Management System
        """

        # Create notification record for patient
        Notification.objects.create(
            recipient=appointment.patient,
            notification_type='appointment_confirmation',
            channel='both',
            subject=subject,
            message=patient_message,
            appointment=appointment,
            status='sent'
        )

        # Send email to patient (best-effort)
        try:
            from_email = config('EMAIL_HOST_USER', default='noreply@micradiology.com')
            recipient_email = appointment.contact_email or getattr(appointment.patient, 'email', None)
            if recipient_email:
                send_mail(subject, patient_message, from_email, [recipient_email], fail_silently=True)
        except Exception:
            pass

        # Notify referring doctor if present
        if appointment.referring_doctor:
            doc_msg = f"Appointment for {appointment.patient.get_full_name()} on {appointment.appointment_date} at {appointment.appointment_time} was marked completed by {completed_by.get_full_name() if completed_by else 'System'}."
            Notification.objects.create(
                recipient=appointment.referring_doctor,
                notification_type='report_ready',
                channel='email',
                subject=subject,
                message=doc_msg,
                appointment=appointment,
                status='sent'
            )
            try:
                from_email = config('EMAIL_HOST_USER', default='noreply@micradiology.com')
                if getattr(appointment.referring_doctor, 'email', None):
                    send_mail(subject, doc_msg, from_email, [appointment.referring_doctor.email], fail_silently=True)
            except Exception:
                pass

        # Notify receptionist(s)
        if appointment.receptionist:
            receptionists = [appointment.receptionist]
        else:
            receptionists = CustomUser.objects.filter(role='receptionist')

        reception_subject = f"[Reception] {subject}"
        reception_message = f"Appointment for {appointment.patient.get_full_name()} on {appointment.appointment_date} at {appointment.appointment_time} was marked completed by {completed_by.get_full_name() if completed_by else 'System'}."

        for r in receptionists:
            Notification.objects.create(
                recipient=r,
                notification_type='report_ready',
                channel='email',
                subject=reception_subject,
                message=reception_message,
                appointment=appointment,
                status='sent'
            )
            try:
                from_email = config('EMAIL_HOST_USER', default='noreply@micradiology.com')
                if getattr(r, 'email', None):
                    send_mail(reception_subject, reception_message, from_email, [r.email], fail_silently=True)
            except Exception:
                pass

    except Appointment.DoesNotExist:
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


@shared_task
def send_appointment_cancelled(appointment_id, cancelled_by_id=None):
    """Notify patient and receptionist that an appointment was cancelled."""
    from apps.appointments.models import Appointment
    from apps.users.models import CustomUser
    from django.core.mail import send_mail
    from decouple import config
    try:
        appointment = Appointment.objects.get(id=appointment_id)

        cancelled_by = None
        if cancelled_by_id:
            try:
                cancelled_by = CustomUser.objects.get(id=cancelled_by_id)
            except Exception:
                cancelled_by = None

        subject = f"Appointment Cancelled - {appointment.scan_type.name if appointment.scan_type else 'Appointment'}"
        patient_message = f"""
Dear {appointment.patient.first_name},

Your appointment scheduled for {appointment.appointment_date} at {appointment.appointment_time} has been cancelled.
Cancelled by: {cancelled_by.get_full_name() if cancelled_by else 'System'}.

If you have questions, please contact reception.

Best regards,
MIC Radiology Management System
        """

        # Create notification record for patient
        Notification.objects.create(
            recipient=appointment.patient,
            notification_type='appointment_cancelled',
            channel='both',
            subject=subject,
            message=patient_message,
            appointment=appointment,
            status='sent'
        )

        # Send email to patient (best-effort)
        try:
            from_email = config('EMAIL_HOST_USER', default='noreply@micradiology.com')
            recipient_email = appointment.contact_email or getattr(appointment.patient, 'email', None)
            if recipient_email:
                send_mail(subject, patient_message, from_email, [recipient_email], fail_silently=True)
        except Exception:
            pass

        # Notify receptionist(s)
        if appointment.receptionist:
            receptionists = [appointment.receptionist]
        else:
            receptionists = CustomUser.objects.filter(role='receptionist')

        reception_subject = f"[Reception] {subject}"
        reception_message = f"Appointment for {appointment.patient.get_full_name()} on {appointment.appointment_date} at {appointment.appointment_time} was cancelled by {cancelled_by.get_full_name() if cancelled_by else 'System'}."

        for r in receptionists:
            Notification.objects.create(
                recipient=r,
                notification_type='appointment_cancelled',
                channel='email',
                subject=reception_subject,
                message=reception_message,
                appointment=appointment,
                status='sent'
            )
            try:
                from_email = config('EMAIL_HOST_USER', default='noreply@micradiology.com')
                if getattr(r, 'email', None):
                    send_mail(reception_subject, reception_message, from_email, [r.email], fail_silently=True)
            except Exception:
                pass

        # Notify referring doctor if present
        if appointment.referring_doctor:
            doc_msg = f"Appointment for {appointment.patient.get_full_name()} on {appointment.appointment_date} at {appointment.appointment_time} was cancelled by {cancelled_by.get_full_name() if cancelled_by else 'System'}."
            Notification.objects.create(
                recipient=appointment.referring_doctor,
                notification_type='appointment_cancelled',
                channel='email',
                subject=subject,
                message=doc_msg,
                appointment=appointment,
                status='sent'
            )
            try:
                from_email = config('EMAIL_HOST_USER', default='noreply@micradiology.com')
                if getattr(appointment.referring_doctor, 'email', None):
                    send_mail(subject, doc_msg, from_email, [appointment.referring_doctor.email], fail_silently=True)
            except Exception:
                pass

    except Appointment.DoesNotExist:
        pass
