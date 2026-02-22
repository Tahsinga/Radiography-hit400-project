from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.notifications.models import Notification
from django.http import JsonResponse

@login_required(login_url='login')
def notification_list(request):
    """List user notifications"""
    # Mark any pending/sent notifications as delivered when the user views their notifications
    user_notifications = request.user.notifications.all()
    unread_qs = user_notifications.filter(status__in=['pending', 'sent'])
    if unread_qs.exists():
        unread_qs.update(status='delivered')

    notifications = request.user.notifications.all().order_by('-created_at')

    context = {
        'notifications': notifications,
        'unread_count': 0,
    }
    return render(request, 'notifications/notification_list.html', context)


@login_required(login_url='login')
def mark_notification_read(request, pk):
    """Mark notification as read"""
    notification = get_object_or_404(Notification, id=pk, recipient=request.user)
    
    if notification.status in ['pending', 'sent']:
        notification.status = 'delivered'
        notification.save()
    
    return redirect('notification_list')


@login_required(login_url='login')
def notification_unread_count(request):
    """Return JSON with count of unread notifications for current user."""
    notifications = request.user.notifications.all()
    count = notifications.filter(status__in=['pending', 'sent']).count()
    return JsonResponse({'unread_count': count})
