from django.urls import path
from apps.notifications import views

urlpatterns = [
    path('list/', views.notification_list, name='notification_list'),
    path('<uuid:pk>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('unread-count/', views.notification_unread_count, name='notification_unread_count'),
]
