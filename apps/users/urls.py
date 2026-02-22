from django.urls import path

from apps.users import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('receptionist-dashboard/', views.receptionist_dashboard, name='receptionist_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.user_list, name='user_list'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
