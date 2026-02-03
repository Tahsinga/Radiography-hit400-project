from django import forms
from apps.reports.models import Report
from apps.analytics.models import Feedback

class ReportUploadForm(forms.ModelForm):
    """Form for radiologists to upload completed reports"""
    
    class Meta:
        model = Report
        fields = ('findings', 'recommendations', 'pdf_file', 'status')
        widgets = {
            'findings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Detailed findings from the scan'
            }),
            'recommendations': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Clinical recommendations'
            }),
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class FeedbackForm(forms.ModelForm):
    """Form for patients to submit feedback"""
    
    class Meta:
        model = Feedback
        fields = ('overall_satisfaction', 'staff_professionalism', 'facility_cleanliness',
                 'report_clarity', 'comments', 'would_recommend')
        widgets = {
            'overall_satisfaction': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'staff_professionalism': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'facility_cleanliness': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'report_clarity': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Please share any additional comments or suggestions'
            }),
            'would_recommend': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['report_clarity'].required = False
        self.fields['comments'].required = False
