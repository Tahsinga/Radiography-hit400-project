from django.db import models
from apps.users.models import CustomUser
from apps.appointments.models import Appointment
import uuid

class Report(models.Model):
    """
    Radiology report after scan is performed
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('reviewed', 'Reviewed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='report')
    
    radiologist = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                                    related_name='reports_created', limit_choices_to={'role': 'staff'})
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Report details
    findings = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='reports/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Tracking
    patient_viewed_at = models.DateTimeField(blank=True, null=True)
    download_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report for {self.appointment.patient.get_full_name()}"
    
    def is_available_for_patient(self):
        """Check if report is ready for patient download"""
        return self.status in ['completed', 'reviewed']


class ReportAccess(models.Model):
    """
    Track who has accessed each report for audit purposes
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='accesses')
    accessed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='report_accesses')
    accessed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        ordering = ['-accessed_at']
    
    def __str__(self):
        return f"{self.report.id} accessed by {self.accessed_by}"
