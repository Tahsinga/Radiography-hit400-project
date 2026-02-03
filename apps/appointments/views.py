from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from apps.appointments.models import Appointment, ScanType
from apps.appointments.forms import AppointmentBookingForm, AppointmentEditForm
from apps.payments.models import Payment, PaymentShortfall

@login_required(login_url='login')
def book_appointment(request):
    """Patient books an appointment"""
    if not request.user.is_patient():
        messages.error(request, 'Only patients can book appointments.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST, request.FILES)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            
            # Validate appointment date
            if appointment.appointment_date < timezone.now().date():
                messages.error(request, 'Cannot book appointment in the past.')
                return render(request, 'appointments/book_appointment.html', {'form': form})
            
            appointment.save()
            
            # Create payment record
            payment = Payment.objects.create(
                appointment=appointment,
                service_charge=appointment.scan_type.base_price,
                payment_method='pending',
                patient_co_payment=appointment.scan_type.base_price
            )
            
            messages.success(request, 'Appointment booked successfully! Please proceed to payment.')
            return redirect('appointment_detail', pk=appointment.id)
    else:
        form = AppointmentBookingForm()
    
    return render(request, 'appointments/book_appointment.html', {'form': form})


@login_required(login_url='login')
def appointment_list(request):
    """List user's appointments"""
    if request.user.is_patient():
        appointments = request.user.appointments.all()
    elif request.user.is_staff_user():
        appointments = Appointment.objects.all()
    elif request.user.is_doctor():
        appointments = Appointment.objects.filter(referring_doctor=request.user)
    else:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Filtering
    status = request.GET.get('status')
    if status:
        appointments = appointments.filter(status=status)
    
    context = {
        'appointments': appointments,
        'statuses': Appointment.STATUS_CHOICES,
        'selected_status': status,
    }
    return render(request, 'appointments/appointment_list.html', context)


@login_required(login_url='login')
def appointment_detail(request, pk):
    """View appointment details"""
    appointment = get_object_or_404(Appointment, id=pk)
    
    # Check permission
    if not (request.user == appointment.patient or request.user.is_staff_user() or 
            request.user == appointment.referring_doctor):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    try:
        payment = appointment.payment  # type: ignore
    except:
        payment = None
    
    try:
        report = appointment.report  # type: ignore
    except:
        report = None
    
    context = {
        'appointment': appointment,
        'payment': payment,
        'report': report,
    }
    return render(request, 'appointments/appointment_detail.html', context)


@login_required(login_url='login')
def cancel_appointment(request, pk):
    """Cancel appointment"""
    appointment = get_object_or_404(Appointment, id=pk)
    
    # Check permission
    if request.user != appointment.patient and not request.user.is_staff_user():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        if not appointment.can_be_cancelled():
            messages.error(request, 'Cannot cancel appointment less than 24 hours before.')
            return redirect('appointment_detail', pk=pk)
        
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully.')
        return redirect('appointment_list')
    
    return render(request, 'appointments/cancel_appointment.html', {'appointment': appointment})


@login_required(login_url='login')
def edit_appointment(request, pk):
    """Edit appointment details (staff only)"""
    if not request.user.is_staff_user():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    appointment = get_object_or_404(Appointment, id=pk)
    
    if request.method == 'POST':
        form = AppointmentEditForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save()
            if appointment.status == 'confirmed':
                appointment.confirmed_by = request.user
                appointment.confirmation_date = timezone.now()
                appointment.save()
            messages.success(request, 'Appointment updated successfully.')
            return redirect('appointment_detail', pk=pk)
    else:
        form = AppointmentEditForm(instance=appointment)
    
    return render(request, 'appointments/edit_appointment.html', 
                 {'form': form, 'appointment': appointment})


@login_required(login_url='login')
def get_appointment_payment_summary(request, pk):
    """Get payment summary for appointment (AJAX)"""
    appointment = get_object_or_404(Appointment, id=pk)
    
    # Check permission
    if request.user != appointment.patient and not request.user.is_staff_user():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Calculate payment details
    service_charge = appointment.scan_type.base_price
    medical_aid_coverage = 0
    
    if request.user.medical_aid_name:
        # Simplified calculation - in production, integrate with medical aid API
        medical_aid_coverage = float(service_charge) * 0.8  # Assume 80% coverage
    
    patient_co_payment = float(service_charge) - medical_aid_coverage
    
    return JsonResponse({
        'service_charge': str(service_charge),
        'medical_aid_coverage': str(medical_aid_coverage),
        'patient_co_payment': str(patient_co_payment),
    })
