from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from apps.appointments.models import Appointment, ScanType
from apps.appointments.forms import AppointmentBookingForm, AppointmentEditForm, ReceptionistActionForm
from apps.appointments.forms import ScanTypeForm
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
            
            # Validate that either scan_type or appointment_description is provided
            if not appointment.scan_type and not appointment.appointment_description:
                messages.error(request, 'Please select a scan type or provide an appointment description.')
                return render(request, 'appointments/book_appointment.html', {'form': form})
            
            # Fill any missing contact/personal snapshot fields from the user profile
            user = request.user
            if not appointment.first_name:
                appointment.first_name = user.first_name
            if not appointment.last_name:
                appointment.last_name = user.last_name
            if not appointment.contact_email:
                appointment.contact_email = user.email
            if not appointment.contact_phone:
                appointment.contact_phone = getattr(user, 'phone_number', '')
            if not appointment.date_of_birth:
                appointment.date_of_birth = getattr(user, 'date_of_birth', None)

            appointment.save()

            # Collect patient personal details to send to reception (use snapshot on appointment)
            full_name = f"{appointment.first_name or ''} {appointment.last_name or ''}".strip() or (request.user.get_full_name() or '')
            email = appointment.contact_email or request.user.email
            phone = appointment.contact_phone or getattr(request.user, 'phone_number', '')
            dob = appointment.date_of_birth or getattr(request.user, 'date_of_birth', None)
            age = ''
            if dob:
                try:
                    today = timezone.now().date()
                    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                except Exception:
                    age = ''
            medical_aid_name = getattr(request.user, 'medical_aid_name', '')
            medical_aid_number = getattr(request.user, 'medical_aid_number', '')
            allergies = appointment.allergies or ''
            other_conditions = appointment.other_conditions or ''

            # Booking details
            scan = appointment.scan_type.name if appointment.scan_type else ''
            appt_date = appointment.appointment_date
            appt_time = appointment.appointment_time
            appt_description = appointment.appointment_description

            # Compose message
            reception_message = (
                f"New appointment booking submitted:\n"
                f"Patient: {full_name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Age: {age}\n"
                f"Date of birth: {dob}\n"
                f"Allergies: {allergies}\n"
                f"Other conditions: {other_conditions}\n"
                f"Medical aid: {medical_aid_name} ({medical_aid_number})\n"
                f"Scan type: {scan}\n"
                f"Date: {appt_date}\n"
                f"Time: {appt_time}\n"
                f"Description: {appt_description}\n"
                f"Appointment ID: {appointment.id}\n"
            )

            # Print to terminal (so developer/receptionist can see submission)
            print(reception_message)

            # Send to reception email via configured backend (console in dev)
            reception_email = getattr(settings, 'RECEPTION_EMAIL', 'reception@example.com')
            try:
                send_mail(
                    subject=f"New Appointment: {full_name} - {appt_date}",
                    message=reception_message,
                    from_email=settings.EMAIL_HOST_USER or 'noreply@example.com',
                    recipient_list=[reception_email],
                    fail_silently=True,
                )
            except Exception:
                # Avoid breaking booking flow if email fails
                pass
            
            # Create payment record only if scan_type is selected
            if appointment.scan_type:
                payment = Payment.objects.create(
                    appointment=appointment,
                    service_charge=appointment.scan_type.base_price,
                    payment_method='pending',
                    patient_co_payment=appointment.scan_type.base_price
                )
            
            messages.success(request, 'Appointment booked successfully!')
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
        # Doctors should see appointments only after receptionist confirms
        appointments = Appointment.objects.filter(referring_doctor=request.user, status='confirmed')
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
    
    # Check permission: allow patient, staff, or referring doctor to cancel
    if not (request.user == appointment.patient or request.user.is_staff_user() or request.user == appointment.referring_doctor):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        if not appointment.can_be_cancelled():
            messages.error(request, 'Cannot cancel appointment less than 24 hours before.')
            return redirect('appointment_detail', pk=pk)
        
        appointment.status = 'cancelled'
        appointment.save()

        # Notify patient and receptionist asynchronously (best-effort)
        try:
            from apps.notifications.tasks import send_appointment_cancelled
            send_appointment_cancelled.delay(str(appointment.id), str(request.user.id))
        except Exception:
            # If Celery/task import fails, try to call synchronously
            try:
                from apps.notifications.tasks import send_appointment_cancelled
                send_appointment_cancelled(str(appointment.id), str(request.user.id))
            except Exception:
                pass

        messages.success(request, 'Appointment cancelled successfully.')
        # If the cancelling user is a doctor, send them to their Cancelled view
        if request.user.is_doctor():
            return redirect('doctor_cancelled')
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
def receptionist_queue(request):
    """List pending appointments for receptionist to review"""
    if not request.user.is_receptionist():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    appointments = Appointment.objects.filter(status='pending')
    status = request.GET.get('status')
    if status:
        appointments = appointments.filter(status=status)

    context = {
        'appointments': appointments,
        'statuses': Appointment.STATUS_CHOICES,
    }
    return render(request, 'appointments/receptionist_queue.html', context)


@login_required(login_url='login')
def manage_scans(request):
    """Receptionist: list and manage available scan types"""
    if not request.user.is_receptionist():
        messages.error(request, 'Access denied. Receptionist access required.')
        return redirect('dashboard')

    scans = ScanType.objects.all().order_by('name')
    return render(request, 'appointments/manage_scans.html', {'scans': scans})


@login_required(login_url='login')
def add_scan(request):
    if not request.user.is_receptionist():
        messages.error(request, 'Access denied. Receptionist access required.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ScanTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Scan type added successfully.')
            return redirect('manage_scans')
    else:
        form = ScanTypeForm()
    return render(request, 'appointments/add_scan.html', {'form': form})


@login_required(login_url='login')
def delete_scan(request, pk):
    if not request.user.is_receptionist():
        messages.error(request, 'Access denied. Receptionist access required.')
        return redirect('dashboard')

    scan = get_object_or_404(ScanType, id=pk)
    if request.method == 'POST':
        scan.delete()
        messages.success(request, 'Scan type removed.')
        return redirect('manage_scans')
    return render(request, 'appointments/confirm_delete_scan.html', {'scan': scan})


@login_required(login_url='login')
def toggle_scan_active(request, pk):
    if not request.user.is_receptionist():
        messages.error(request, 'Access denied. Receptionist access required.')
        return redirect('dashboard')

    scan = get_object_or_404(ScanType, id=pk)
    scan.is_active = not scan.is_active
    scan.save()
    messages.success(request, 'Scan availability updated.')
    return redirect('manage_scans')


@login_required(login_url='login')
def manage_appointment_by_receptionist(request, pk):
    """Receptionist accepts/declines/writes a note for an appointment"""
    if not request.user.is_receptionist():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    appointment = get_object_or_404(Appointment, id=pk)

    if request.method == 'POST':
        old_status = appointment.status
        form = ReceptionistActionForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.receptionist = request.user
            # If receptionist confirms, set confirmed_by and confirmation_date
            if appointment.status == 'confirmed':
                appointment.confirmed_by = request.user
                appointment.confirmation_date = timezone.now()

            appointment.save()

            # If status changed, trigger notifications accordingly
            new_status = appointment.status
            if old_status != new_status:
                # Confirmed -> send confirmation notification to patient
                if new_status == 'confirmed':
                    try:
                        from apps.notifications.tasks import send_appointment_confirmation
                        send_appointment_confirmation.delay(str(appointment.id))
                    except Exception:
                        try:
                            from apps.notifications.tasks import send_appointment_confirmation
                            send_appointment_confirmation(str(appointment.id))
                        except Exception:
                            pass

                # Cancelled -> notify patient, receptionist(s) and referring doctor
                if new_status == 'cancelled':
                    try:
                        from apps.notifications.tasks import send_appointment_cancelled
                        send_appointment_cancelled.delay(str(appointment.id), str(request.user.id))
                    except Exception:
                        try:
                            from apps.notifications.tasks import send_appointment_cancelled
                            send_appointment_cancelled(str(appointment.id), str(request.user.id))
                        except Exception:
                            pass

                # Completed -> notify patient, doctor, reception
                if new_status == 'completed':
                    try:
                        from apps.notifications.tasks import send_appointment_completed
                        send_appointment_completed.delay(str(appointment.id), str(request.user.id))
                    except Exception:
                        try:
                            from apps.notifications.tasks import send_appointment_completed
                            send_appointment_completed(str(appointment.id), str(request.user.id))
                        except Exception:
                            pass

            messages.success(request, 'Appointment updated.')
            return redirect('receptionist_queue')
    else:
        form = ReceptionistActionForm(instance=appointment)

    return render(request, 'appointments/manage_by_receptionist.html', {
        'form': form, 'appointment': appointment
    })

@login_required(login_url='login')
def mark_appointment_completed(request, pk):
    """Mark an appointment as completed. Allowed for referring doctor, receptionist, or staff."""
    appointment = get_object_or_404(Appointment, id=pk)

    # Permission: referring doctor, receptionist, or staff
    if not (request.user == appointment.referring_doctor or request.user.is_receptionist() or request.user.is_staff_user()):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    if request.method == 'POST':
        appointment.status = 'completed'
        appointment.save()
        messages.success(request, 'Appointment marked as completed.')
        # Redirect back to where the user came from if possible
        # Notify patient/doctor/receptionist asynchronously
        try:
            from apps.notifications.tasks import send_appointment_completed
            send_appointment_completed.delay(str(appointment.id), str(request.user.id))
        except Exception:
            try:
                from apps.notifications.tasks import send_appointment_completed
                send_appointment_completed(str(appointment.id), str(request.user.id))
            except Exception:
                pass

        ref = request.META.get('HTTP_REFERER')
        if ref:
            return redirect(ref)
        if request.user.is_doctor():
            return redirect('doctor_dashboard')
        return redirect('appointment_detail', pk=pk)

    # If GET, show a simple confirmation page or redirect
    return render(request, 'appointments/confirm_mark_completed.html', {'appointment': appointment})


@login_required(login_url='login')
def doctor_completed_appointments(request):
    """List completed appointments for the referring doctor."""
    if not request.user.is_doctor():
        messages.error(request, 'Access denied. Doctor access required.')
        return redirect('dashboard')

    completed = Appointment.objects.filter(referring_doctor=request.user, status='completed').order_by('-confirmation_date', '-appointment_date')

    context = {
        'completed_appointments': completed,
    }
    return render(request, 'users/doctor_completed.html', context)


@login_required(login_url='login')
def doctor_cancelled_appointments(request):
    """List cancelled appointments for the referring doctor."""
    if not request.user.is_doctor():
        messages.error(request, 'Access denied. Doctor access required.')
        return redirect('dashboard')

    cancelled = Appointment.objects.filter(referring_doctor=request.user, status='cancelled').order_by('-updated_at', '-appointment_date')

    context = {
        'cancelled_appointments': cancelled,
    }
    return render(request, 'users/doctor_cancelled.html', context)


@login_required(login_url='login')
def get_appointment_payment_summary(request, pk):
    """Get payment summary for appointment (AJAX)"""
    appointment = get_object_or_404(Appointment, id=pk)
    
    # Check permission
    if request.user != appointment.patient and not request.user.is_staff_user():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Calculate payment details (guard against missing scan_type)
    if appointment.scan_type and getattr(appointment.scan_type, 'base_price', None) is not None:
        service_charge = float(appointment.scan_type.base_price)
    else:
        service_charge = 0.0

    medical_aid_coverage = 0.0
    # Simplified calculation - in production, integrate with medical aid API
    if service_charge and request.user.medical_aid_name:
        medical_aid_coverage = service_charge * 0.8  # Assume 80% coverage

    patient_co_payment = service_charge - medical_aid_coverage
    
    return JsonResponse({
        'service_charge': str(service_charge),
        'medical_aid_coverage': str(medical_aid_coverage),
        'patient_co_payment': str(patient_co_payment),
    })
