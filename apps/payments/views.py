from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from apps.appointments.models import Appointment
from apps.payments.models import Payment, PaymentShortfall

@login_required(login_url='login')
def process_payment(request, appointment_id):
    """Process payment for appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check permission
    if request.user != appointment.patient and not request.user.is_staff_user():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    try:
        payment = appointment.payment  # type: ignore
    except:
        messages.error(request, 'No payment record found for this appointment.')
        return redirect('appointment_detail', pk=appointment_id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return redirect('process_payment', appointment_id=appointment_id)
        
        payment.payment_method = payment_method
        payment.status = 'processing'
        payment.save()
        
        # Simulate payment processing
        # In production, integrate with actual payment gateway
        messages.success(request, 'Payment processing. Please wait...')
        
        # Update payment status
        payment.status = 'completed'
        payment.save()
        
        # Send confirmation notification
        from apps.notifications.tasks import send_payment_confirmation
        send_payment_confirmation.delay(payment.id)
        
        messages.success(request, 'Payment completed successfully!')
        return redirect('appointment_detail', pk=appointment_id)
    
    # Calculate shortfall if any
    shortfall = None
    try:
        shortfall = payment.shortfall
    except PaymentShortfall.DoesNotExist:
        pass
    
    context = {
        'appointment': appointment,
        'payment': payment,
        'shortfall': shortfall,
    }
    return render(request, 'payments/process_payment.html', context)


@login_required(login_url='login')
def payment_status(request, appointment_id):
    """Get payment status (AJAX)"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check permission
    if request.user != appointment.patient and not request.user.is_staff_user():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        payment = appointment.payment  # type: ignore
        return JsonResponse({
            'status': payment.status,
            'is_paid': payment.is_paid(),
            'amount': str(payment.service_charge),
        })
    except:
        return JsonResponse({'error': 'Payment not found'}, status=404)


@login_required(login_url='login')
def payment_list(request):
    """List payments (admin only)"""
    if not request.user.is_staff_user() and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    payments = Payment.objects.all()
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        payments = payments.filter(status=status)
    
    context = {
        'payments': payments,
        'statuses': Payment.STATUS_CHOICES,
        'selected_status': status,
    }
    return render(request, 'payments/payment_list.html', context)
