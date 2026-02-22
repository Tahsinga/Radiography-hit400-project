from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from apps.users.forms import PatientRegistrationForm, DoctorRegistrationForm, ReceptionistRegistrationForm, CustomUserChangeForm
from apps.users.models import CustomUser

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def edit_profile(request):
    """Edit user profile view"""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

def home(request):
    """Home page - redirects to login or dashboard"""
    if request.user.is_authenticated:
        response = redirect('dashboard')
    else:
        response = redirect('login')
    
    # Prevent caching of authentication state
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@require_http_methods(["GET", "POST"])
def register(request):
    """User registration view with role selection"""
    if request.method == 'POST':
        user_role = request.POST.get('role', 'patient')
        if user_role == 'doctor':
            form = DoctorRegistrationForm(request.POST, request.FILES)
        elif user_role == 'receptionist':
            form = ReceptionistRegistrationForm(request.POST, request.FILES)
        else:
            form = PatientRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            # Force the correct role regardless of form data
            if user_role == 'doctor':
                user.role = 'doctor'
            elif user_role == 'receptionist':
                user.role = 'receptionist'
            else:
                user.role = 'patient'
            user.save()
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PatientRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'users/login.html')


@login_required(login_url='login')
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    """Main dashboard - role-based redirect"""
    if request.user.is_patient():
        return redirect('patient_dashboard')
    elif request.user.is_staff_user():
        return redirect('staff_dashboard')
    elif request.user.is_receptionist():
        return redirect('receptionist_dashboard')
    elif request.user.is_doctor():
        return redirect('doctor_dashboard')
    return redirect('login')


@login_required(login_url='login')
def patient_dashboard(request):
    """Patient dashboard"""
    if not request.user.is_patient():
        messages.error(request, 'Access denied. Patient access required.')
        return redirect('dashboard')
    
    from apps.appointments.models import Appointment
    appointments = request.user.appointments.all()
    upcoming_appointments = [a for a in appointments if a.is_upcoming()]
    completed_appointments = appointments.filter(status='completed')
    
    context = {
        'total_appointments': appointments.count(),
        'upcoming_appointments': upcoming_appointments,
        'completed_appointments': completed_appointments,
    }
    return render(request, 'users/patient_dashboard.html', context)


@login_required(login_url='login')
def staff_dashboard(request):
    """Staff/Admin dashboard"""
    if not request.user.is_staff_user():
        messages.error(request, 'Access denied. Staff access required.')
        return redirect('dashboard')
    
    from apps.appointments.models import Appointment
    from apps.payments.models import Payment
    
    today_appointments = Appointment.objects.filter(appointment_date__date=__import__('django.utils.timezone', fromlist=['now'])().now().date())
    pending_appointments = Appointment.objects.filter(status='pending')
    pending_payments = Payment.objects.filter(status='pending')
    
    context = {
        'today_appointments': today_appointments,
        'pending_appointments': pending_appointments,
        'pending_payments': pending_payments,
    }
    return render(request, 'users/staff_dashboard.html', context)


@login_required(login_url='login')
def receptionist_dashboard(request):
    """Receptionist dashboard"""
    if not request.user.is_receptionist():
        messages.error(request, 'Access denied. Receptionist access required.')
        return redirect('dashboard')
    
    from apps.appointments.models import Appointment
    
    pending_appointments = Appointment.objects.filter(status='pending')
    confirmed_appointments = Appointment.objects.filter(status='confirmed')
    total_handled = Appointment.objects.filter(receptionist=request.user)
    
    context = {
        'pending_count': pending_appointments.count(),
        'confirmed_count': confirmed_appointments.count(),
        'total_handled': total_handled.count(),
        'pending_appointments': pending_appointments[:10],  # Show last 10
    }
    return render(request, 'users/receptionist_dashboard.html', context)


@login_required(login_url='login')
def doctor_dashboard(request):
    """Referral doctor dashboard"""
    if not request.user.is_doctor():
        messages.error(request, 'Access denied. Doctor access required.')
        return redirect('dashboard')
    
    from apps.appointments.models import Appointment
    # Show active referrals (exclude completed and cancelled) on dashboard
    referrals = Appointment.objects.filter(referring_doctor=request.user).exclude(status__in=['completed', 'cancelled'])
    completed_referrals = Appointment.objects.filter(referring_doctor=request.user, status='completed')

    context = {
        'total_referrals': referrals.count(),
        'completed_referrals': completed_referrals,
        'referrals': referrals,  # non-completed referrals for listing
    }
    return render(request, 'users/doctor_dashboard.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})


@login_required(login_url='login')
def user_list(request):
    """List users (admin only)"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})
