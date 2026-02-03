from django.db import models
from apps.users.models import CustomUser
from apps.appointments.models import Appointment
import uuid

class Feedback(models.Model):
    """
    Patient feedback and satisfaction ratings
    """
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='feedback')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='feedback_submitted')
    
    # Ratings
    overall_satisfaction = models.IntegerField(choices=RATING_CHOICES)
    staff_professionalism = models.IntegerField(choices=RATING_CHOICES)
    facility_cleanliness = models.IntegerField(choices=RATING_CHOICES)
    report_clarity = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    
    # Feedback
    comments = models.TextField(blank=True)
    would_recommend = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback from {self.patient.get_full_name()}"
    
    def get_average_rating(self):
        """Calculate average rating across all categories"""
        ratings = [
            self.overall_satisfaction,
            self.staff_professionalism,
            self.facility_cleanliness,
        ]
        if self.report_clarity:
            ratings.append(self.report_clarity)
        return sum(ratings) / len(ratings) if ratings else 0
