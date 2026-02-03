from django.db import models
from apps.appointments.models import Appointment
from apps.users.models import CustomUser
import uuid

class Notification(models.Model):
    """
    Notification tracking for SMS and Email
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('appointment_confirmation', 'Appointment Confirmation'),
        ('appointment_reminder', 'Appointment Reminder'),
        ('payment_reminder', 'Payment Reminder'),
        ('report_ready', 'Report Ready'),
        ('appointment_cancelled', 'Appointment Cancelled'),
        ('payment_shortfall', 'Payment Shortfall'),
    ]
    
    CHANNEL_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('both', 'SMS & Email'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('delivered', 'Delivered'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='notifications')
    
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    sent_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    
    external_id = models.CharField(max_length=100, blank=True)  # From SMS/Email provider
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'status']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f"{self.get_notification_type_display()} to {self.recipient.get_full_name()}"  # type: ignore


class NotificationTemplate(models.Model):
    """
    Reusable notification templates
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    notification_type = models.CharField(max_length=30)
    
    sms_template = models.TextField(blank=True, help_text="Use {{variable}} for dynamic content")
    email_subject_template = models.CharField(max_length=200, blank=True)
    email_body_template = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
