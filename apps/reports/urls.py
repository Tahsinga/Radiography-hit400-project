from django.urls import path
from apps.reports import views

urlpatterns = [
    path('<uuid:pk>/upload/', views.upload_report, name='upload_report'),
    path('<uuid:pk>/view/', views.view_report, name='view_report'),
    path('<uuid:pk>/download/', views.download_report, name='download_report'),
    path('<uuid:pk>/feedback/', views.submit_feedback, name='submit_feedback'),
]
