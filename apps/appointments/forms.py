from django import forms
from django.forms import ModelChoiceField
from apps.appointments.models import Appointment, ScanType
from apps.users.models import CustomUser

class AppointmentBookingForm(forms.ModelForm):
    """Form for booking appointments"""
    
    referring_doctor = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='doctor'),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'doctorSelect'
        })
    )
    
    class Meta:
        model = Appointment
        fields = (
            'first_name', 'last_name', 'contact_phone', 'contact_email', 'date_of_birth', 'allergies', 'other_conditions',
            'scan_type', 'referring_doctor', 'appointment_date', 'appointment_time', 'appointment_description', 'referral_document', 'clinical_notes'
        )
        widgets = {
            'scan_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'scanType'
            }),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'List any allergies'}),
            'other_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any other diseases or conditions'}),
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': '{% now "Y-m-d" %}'
            }),
            'appointment_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'appointment_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'E.g., Follow-up check, Routine scan, etc.'
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
        self.fields['scan_type'].required = False
        self.fields['referring_doctor'].required = False
        self.fields['appointment_description'].required = False
        self.fields['referral_document'].required = False
        self.fields['clinical_notes'].required = False
        # Make personal/contact fields optional but present
        for f in ('first_name', 'last_name', 'contact_phone', 'contact_email', 'date_of_birth', 'allergies', 'other_conditions'):
            if f in self.fields:
                self.fields[f].required = False


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


class ReceptionistActionForm(forms.ModelForm):
    """Form for receptionist to accept/decline and add a note"""
    class Meta:
        model = Appointment
        fields = ('status', 'receptionist_note')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'receptionist_note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add a note for the patient'
            }),
        }


class ScanTypeForm(forms.ModelForm):
    """Form for receptionist to add or edit ScanType"""
    class Meta:
        model = ScanType
        fields = ('name', 'description', 'base_price', 'estimated_duration_minutes', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estimated_duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
