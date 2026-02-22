from django.urls import path
from apps.appointments import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('list/', views.appointment_list, name='appointment_list'),
    path('reception/requests/', views.receptionist_queue, name='receptionist_queue'),
    path('<uuid:pk>/', views.appointment_detail, name='appointment_detail'),
    path('<uuid:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('<uuid:pk>/edit/', views.edit_appointment, name='edit_appointment'),
    path('<uuid:pk>/reception/manage/', views.manage_appointment_by_receptionist, name='manage_appointment_by_receptionist'),
    path('<uuid:pk>/mark-completed/', views.mark_appointment_completed, name='mark_appointment_completed'),
    path('doctor/completed/', views.doctor_completed_appointments, name='doctor_completed'),
    path('doctor/cancelled/', views.doctor_cancelled_appointments, name='doctor_cancelled'),
    path('scans/', views.manage_scans, name='manage_scans'),
    path('scans/add/', views.add_scan, name='add_scan'),
    path('scans/<uuid:pk>/delete/', views.delete_scan, name='delete_scan'),
    path('scans/<uuid:pk>/toggle/', views.toggle_scan_active, name='toggle_scan_active'),
    path('<uuid:pk>/payment-summary/', views.get_appointment_payment_summary, name='payment_summary'),
]
