from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from apps.appointments.models import Appointment
from apps.reports.models import Report, ReportAccess
from apps.reports.forms import ReportUploadForm, FeedbackForm
from apps.analytics.models import Feedback

@login_required(login_url='login')
def upload_report(request, pk):
    """Upload report (radiologist only)"""
    if not request.user.is_staff_user():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    appointment = get_object_or_404(Appointment, id=pk)
    
    try:
        report = appointment.report  # type: ignore
    except Report.DoesNotExist:
        report = None
    
    if request.method == 'POST':
        form = ReportUploadForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            if not report.appointment:
                report.appointment = appointment
            report.radiologist = request.user
            
            from django.utils import timezone
            if report.status == 'completed':
                report.completed_at = timezone.now()
            
            report.save()
            messages.success(request, 'Report uploaded successfully!')
            
            # Send notification to patient and doctor
            from apps.notifications.tasks import send_report_ready_notification
            send_report_ready_notification.delay(report.id)
            
            return redirect('appointment_detail', pk=pk)
    else:
        form = ReportUploadForm(instance=report)
    
    return render(request, 'reports/upload_report.html', 
                 {'form': form, 'appointment': appointment})


@login_required(login_url='login')
def view_report(request, pk):
    """View report"""
    report = get_object_or_404(Report, id=pk)
    
    # Check permission
    appointment = report.appointment
    if not (request.user == appointment.patient or request.user.is_staff_user() or 
            request.user == appointment.referring_doctor):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if not report.is_available_for_patient() and request.user == appointment.patient:
        messages.error(request, 'Report is not yet available.')
        return redirect('appointment_detail', pk=appointment.id)
    
    # Track access
    ip_address = get_client_ip(request)
    ReportAccess.objects.create(
        report=report,
        accessed_by=request.user,
        ip_address=ip_address
    )
    
    # Update patient viewed time
    if request.user == appointment.patient:
        from django.utils import timezone
        if not report.patient_viewed_at:
            report.patient_viewed_at = timezone.now()
            report.save()
    
    return render(request, 'reports/view_report.html', {'report': report})


@login_required(login_url='login')
def download_report(request, pk):
    """Download report PDF"""
    report = get_object_or_404(Report, id=pk)
    
    # Check permission
    appointment = report.appointment
    if not (request.user == appointment.patient or request.user.is_staff_user() or 
            request.user == appointment.referring_doctor):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if not report.pdf_file:
        messages.error(request, 'Report PDF not available.')
        return redirect('view_report', pk=pk)
    
    report.download_count += 1
    report.save()
    
    return FileResponse(report.pdf_file.open('rb'), 
                       content_type='application/pdf',
                       as_attachment=True,
                       filename=f'report_{report.id}.pdf')


@login_required(login_url='login')
def submit_feedback(request, pk):
    """Submit feedback for appointment"""
    if not request.user.is_patient():
        messages.error(request, 'Only patients can submit feedback.')
        return redirect('dashboard')
    
    appointment = get_object_or_404(Appointment, id=pk)
    
    if appointment.patient != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Check if feedback already exists
    try:
        feedback = appointment.feedback  # type: ignore
        form_instance = feedback
    except Feedback.DoesNotExist:
        form_instance = None
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=form_instance)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.appointment = appointment
            feedback.patient = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('appointment_detail', pk=pk)
    else:
        form = FeedbackForm(instance=form_instance)
    
    return render(request, 'reports/submit_feedback.html', 
                 {'form': form, 'appointment': appointment})


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
