from django import forms
from django.forms import ModelChoiceField
from apps.appointments.models import Appointment, ScanType

class AppointmentBookingForm(forms.ModelForm):
    """Form for booking appointments"""
    
    class Meta:
        model = Appointment
        fields = ('scan_type', 'appointment_date', 'appointment_time', 'referral_document', 'clinical_notes')
        widgets = {
            'scan_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'scanType'
            }),
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': '{% now "Y-m-d" %}'
            }),
            'appointment_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'referral_document': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.png'
            }),
            'clinical_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Any additional clinical notes or concerns?'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter active scan types
        scan_field = self.fields.get('scan_type')
        if isinstance(scan_field, ModelChoiceField):
            scan_field.queryset = ScanType.objects.filter(is_active=True)
        self.fields['referral_document'].required = False
        self.fields['clinical_notes'].required = False


class AppointmentEditForm(forms.ModelForm):
    """Form for editing appointment details (staff only)"""
    
    class Meta:
        model = Appointment
        fields = ('status', 'clinical_notes')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'clinical_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
        }
