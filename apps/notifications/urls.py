from django.urls import path
from apps.notifications import views

urlpatterns = [
    path('list/', views.notification_list, name='notification_list'),
    path('<uuid:pk>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
]
