from django.urls import path
from apps.payments import views

urlpatterns = [
    path('<uuid:appointment_id>/process/', views.process_payment, name='process_payment'),
    path('<uuid:appointment_id>/status/', views.payment_status, name='payment_status'),
    path('list/', views.payment_list, name='payment_list'),
]
