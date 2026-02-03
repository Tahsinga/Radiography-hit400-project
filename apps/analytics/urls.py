from django.urls import path
from apps.analytics import views

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
    path('revenue/', views.revenue_report, name='revenue_report'),
    path('feedback/', views.feedback_analysis, name='feedback_analysis'),
]
