from django.contrib import admin
from apps.analytics.models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('patient', 'overall_satisfaction', 'would_recommend', 'created_at')
    list_filter = ('overall_satisfaction', 'would_recommend', 'created_at')
    search_fields = ('patient__first_name', 'patient__email')
    readonly_fields = ('created_at',)
