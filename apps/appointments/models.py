from django.db import models
from apps.users.models import CustomUser
from django.utils import timezone
from datetime import timedelta
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.payments.models import Payment
    from apps.reports.models import Report

class ScanType(models.Model):
    """
    Different types of radiology scans offered
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)  # e.g., X-Ray, CT Scan, MRI, Ultrasound
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_duration_minutes = models.IntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Appointment(models.Model):
    """
    Patient appointment for radiology services
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    referring_doctor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='referred_appointments', limit_choices_to={'role': 'doctor'})
    scan_type = models.ForeignKey(ScanType, on_delete=models.PROTECT, related_name='appointments')
    
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    referral_document = models.FileField(upload_to='referrals/', blank=True, null=True)
    clinical_notes = models.TextField(blank=True)
    
    confirmed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='confirmed_appointments', limit_choices_to={'role': 'staff'})
    confirmation_date = models.DateTimeField(blank=True, null=True)
    
    reminder_sent = models.BooleanField(default=False)
    reminder_sent_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
        indexes = [
            models.Index(fields=['patient', 'appointment_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.scan_type.name} on {self.appointment_date}"
    
    def is_upcoming(self):
        from django.utils import timezone
        now = timezone.now().date()
        return self.appointment_date > now and self.status != 'cancelled'
    
    def is_today(self):
        from django.utils import timezone
        return self.appointment_date == timezone.now().date()
    
    def can_be_cancelled(self):
        """Check if appointment can be cancelled (must be at least 24 hours away)"""
        if self.status in ['cancelled', 'completed', 'no_show']:
            return False
        from django.utils import timezone
        appointment_datetime = timezone.make_aware(
            timezone.datetime.combine(self.appointment_date, self.appointment_time)
        )
        time_until_appointment = appointment_datetime - timezone.now()
        return time_until_appointment > timedelta(hours=24)


class MedicalAidCoverage(models.Model):
    """
    Medical aid coverage details for payment calculations
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medical_aid_name = models.CharField(max_length=100, unique=True)
    coverage_percentage = models.IntegerField(default=80)  # Percentage of cost covered
    requires_authorization = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['medical_aid_name']
    
    def __str__(self):
        return f"{self.medical_aid_name} - {self.coverage_percentage}%"
