from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta
from apps.appointments.models import Appointment, ScanType
from apps.payments.models import Payment
from apps.analytics.models import Feedback
import json

@login_required(login_url='login')
def analytics_dashboard(request):
    """Analytics dashboard (admin only)"""
    if not request.user.is_staff_user() and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Time range filter
    days = int(request.GET.get('days', 30))
    start_date = timezone.now().date() - timedelta(days=days)
    
    # Appointments data
    appointments = Appointment.objects.filter(appointment_date__gte=start_date)
    
    total_appointments = appointments.count()
    completed_appointments = appointments.filter(status='completed').count()
    missed_appointments = appointments.filter(status='no_show').count()
    cancelled_appointments = appointments.filter(status='cancelled').count()
    
    missed_rate = (missed_appointments / total_appointments * 100) if total_appointments > 0 else 0
    completion_rate = (completed_appointments / total_appointments * 100) if total_appointments > 0 else 0
    
    # Scan types breakdown
    scan_breakdown = appointments.values('scan_type__name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Revenue data
    payments = Payment.objects.filter(created_at__gte=start_date)
    total_revenue = payments.filter(status='completed').aggregate(Sum('service_charge'))['service_charge__sum'] or 0
    pending_revenue = payments.filter(status='pending').aggregate(Sum('service_charge'))['service_charge__sum'] or 0
    
    # Feedback data
    feedback_records = Feedback.objects.filter(created_at__gte=start_date)
    avg_satisfaction = feedback_records.aggregate(Avg('overall_satisfaction'))['overall_satisfaction__avg'] or 0
    would_recommend_count = feedback_records.filter(would_recommend=True).count()
    
    # Daily appointments trend
    daily_data = appointments.extra(
        select={'date': 'DATE(appointment_date)'}
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    # Payment shortfalls
    shortfalls = payments.filter(shortfall__isnull=False).aggregate(
        total_shortfall=Sum('shortfall__shortfall_amount'),
        count=Count('shortfall')
    )
    
    context = {
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
        'missed_appointments': missed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'missed_rate': round(missed_rate, 1),
        'completion_rate': round(completion_rate, 1),
        'scan_breakdown': list(scan_breakdown),
        'total_revenue': total_revenue,
        'pending_revenue': pending_revenue,
        'avg_satisfaction': round(avg_satisfaction, 1),
        'would_recommend_rate': round((would_recommend_count / feedback_records.count() * 100) if feedback_records.count() > 0 else 0, 1),
        'daily_data_json': json.dumps(list(daily_data)),
        'shortfalls': shortfalls,
        'time_range_days': days,
    }
    
    return render(request, 'analytics/dashboard.html', context)


@login_required(login_url='login')
def revenue_report(request):
    """Revenue analysis report"""
    if not request.user.is_staff_user() and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    days = int(request.GET.get('days', 90))
    start_date = timezone.now().date() - timedelta(days=days)
    
    payments = Payment.objects.filter(created_at__gte=start_date)
    
    # Revenue by scan type
    revenue_by_scan = payments.filter(status='completed').values(
        'appointment__scan_type__name'
    ).annotate(
        total_revenue=Sum('service_charge'),
        count=Count('id'),
        avg_amount=Avg('service_charge')
    ).order_by('-total_revenue')
    
    # Revenue trend
    daily_revenue = payments.filter(status='completed').extra(
        select={'date': 'DATE(created_at)'}
    ).values('date').annotate(
        total=Sum('service_charge'),
        count=Count('id')
    ).order_by('date')
    
    # Payment method breakdown
    payment_method_breakdown = payments.filter(status='completed').values(
        'payment_method'
    ).annotate(
        total=Sum('service_charge'),
        count=Count('id')
    ).order_by('-total')
    
    context = {
        'revenue_by_scan': list(revenue_by_scan),
        'daily_revenue_json': json.dumps(list(daily_revenue)),
        'payment_method_breakdown': list(payment_method_breakdown),
        'time_range_days': days,
    }
    
    return render(request, 'analytics/revenue_report.html', context)


@login_required(login_url='login')
def feedback_analysis(request):
    """Analyze patient feedback"""
    if not request.user.is_staff_user() and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    days = int(request.GET.get('days', 30))
    start_date = timezone.now().date() - timedelta(days=days)
    
    feedback = Feedback.objects.filter(created_at__gte=start_date)
    
    # Average ratings
    avg_overall = feedback.aggregate(Avg('overall_satisfaction'))['overall_satisfaction__avg'] or 0
    avg_staff = feedback.aggregate(Avg('staff_professionalism'))['staff_professionalism__avg'] or 0
    avg_cleanliness = feedback.aggregate(Avg('facility_cleanliness'))['facility_cleanliness__avg'] or 0
    avg_report = feedback.aggregate(Avg('report_clarity'))['report_clarity__avg'] or 0
    
    # Rating distribution
    rating_distribution = {}
    for rating in range(1, 6):
        rating_distribution[rating] = feedback.filter(overall_satisfaction=rating).count()
    
    # Recommendations
    would_recommend = feedback.filter(would_recommend=True).count()
    would_not_recommend = feedback.filter(would_recommend=False).count()
    
    context = {
        'total_feedback': feedback.count(),
        'avg_overall': round(avg_overall, 1),
        'avg_staff': round(avg_staff, 1),
        'avg_cleanliness': round(avg_cleanliness, 1),
        'avg_report': round(avg_report, 1),
        'rating_distribution': rating_distribution,
        'would_recommend': would_recommend,
        'would_not_recommend': would_not_recommend,
        'recommend_rate': round((would_recommend / feedback.count() * 100) if feedback.count() > 0 else 0, 1),
        'time_range_days': days,
    }
    
    return render(request, 'analytics/feedback_analysis.html', context)
