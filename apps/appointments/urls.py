from django.urls import path
from apps.appointments import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('list/', views.appointment_list, name='appointment_list'),
    path('<uuid:pk>/', views.appointment_detail, name='appointment_detail'),
    path('<uuid:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('<uuid:pk>/edit/', views.edit_appointment, name='edit_appointment'),
    path('<uuid:pk>/payment-summary/', views.get_appointment_payment_summary, name='payment_summary'),
]
