from django.db import models
from apps.users.models import CustomUser
from apps.appointments.models import Appointment
from decimal import Decimal
import uuid

class Payment(models.Model):
    """
    Payment tracking for appointments
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash at Facility'),
        ('insurance', 'Insurance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment')
    
    # Amount breakdown
    service_charge = models.DecimalField(max_digits=10, decimal_places=2)
    medical_aid_coverage_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    patient_co_payment = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Transaction info
    transaction_id = models.CharField(max_length=100, blank=True, unique=True)
    payment_gateway = models.CharField(max_length=50, blank=True)  # e.g., Stripe, PayPal
    
    # Processing
    processed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='payments_processed', limit_choices_to={'role': 'staff'})
    processed_at = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['appointment']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Payment {self.transaction_id or self.id} - {self.get_status_display()}"  # type: ignore
    
    def is_paid(self):
        return self.status == 'completed'
    
    def get_total_amount(self):
        return self.service_charge
    
    def get_patient_amount_due(self):
        """Calculate what patient needs to pay after medical aid coverage"""
        return self.patient_co_payment


class PaymentShortfall(models.Model):
    """
    Track situations where medical aid doesn't cover full cost
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='shortfall')
    
    expected_coverage = models.DecimalField(max_digits=10, decimal_places=2)
    actual_coverage = models.DecimalField(max_digits=10, decimal_places=2)
    shortfall_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    reason = models.TextField()
    patient_notified = models.BooleanField(default=False)
    notified_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Shortfall: {self.shortfall_amount} for {self.payment.appointment.patient}"
