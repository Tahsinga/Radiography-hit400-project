from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator
import uuid

class CustomUser(AbstractUser):
    """
    Custom user model with role-based access control
    """
    USER_ROLES = [
        ('patient', 'Patient'),
        ('staff', 'Radiology Staff'),
        ('receptionist', 'Receptionist'),
        ('doctor', 'Referral Doctor'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='patient')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # Doctor specific fields
    license_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    specialization = models.CharField(max_length=100, blank=True)
    hospital_affiliation = models.CharField(max_length=200, blank=True)
    
    # Patient specific fields
    medical_aid_number = models.CharField(max_length=50, blank=True, null=True)
    medical_aid_name = models.CharField(max_length=100, blank=True)
    
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"  # type: ignore
    
    def is_patient(self):
        return self.role == 'patient'
    
    def is_staff_user(self):
        return self.role == 'staff'

    def is_receptionist(self):
        return self.role == 'receptionist'
    
    def is_doctor(self):
        return self.role == 'doctor'
