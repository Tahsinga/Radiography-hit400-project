from django.contrib import admin
from apps.reports.models import Report, ReportAccess

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'radiologist', 'status', 'completed_at', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('appointment__patient__first_name', 'appointment__patient__email')
    readonly_fields = ('created_at', 'updated_at', 'completed_at', 'patient_viewed_at')


@admin.register(ReportAccess)
class ReportAccessAdmin(admin.ModelAdmin):
    list_display = ('report', 'accessed_by', 'accessed_at', 'ip_address')
    list_filter = ('accessed_at',)
    readonly_fields = ('accessed_at',)
