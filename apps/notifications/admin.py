from django.contrib import admin
from apps.notifications.models import Notification, NotificationTemplate

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'channel', 'status', 'created_at')
    list_filter = ('status', 'notification_type', 'channel', 'created_at')
    search_fields = ('recipient__email', 'subject')
    readonly_fields = ('created_at', 'sent_at', 'delivered_at')


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'notification_type', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
