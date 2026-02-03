from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.notifications.models import Notification

@login_required(login_url='login')
def notification_list(request):
    """List user notifications"""
    notifications = request.user.notifications.all().order_by('-created_at')
    
    context = {
        'notifications': notifications,
        'unread_count': notifications.filter(status__in=['pending', 'sent']).count(),
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
