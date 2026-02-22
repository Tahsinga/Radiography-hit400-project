from django.contrib import admin
from apps.appointments.models import Appointment, ScanType, MedicalAidCoverage

@admin.register(ScanType)
class ScanTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'estimated_duration_minutes', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'first_name', 'last_name', 'contact_phone', 'scan_type', 'referring_doctor', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date', 'scan_type', 'referring_doctor')
    search_fields = ('patient__first_name', 'patient__last_name', 'patient__email')
    readonly_fields = ('created_at', 'updated_at', 'confirmation_date', 'reminder_sent_at')
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient', 'first_name', 'last_name', 'contact_phone', 'contact_email', 'date_of_birth', 'allergies', 'other_conditions', 'referring_doctor')
        }),
        ('Appointment Details', {
            'fields': ('scan_type', 'appointment_description', 'appointment_date', 'appointment_time', 'status')
        }),
        ('Medical Information', {
            'fields': ('clinical_notes', 'referral_document')
        }),
        ('Receptionist Information', {
            'fields': ('receptionist', 'receptionist_note', 'confirmed_by')
        }),
        ('Reminders', {
            'fields': ('reminder_sent', 'reminder_sent_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmation_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MedicalAidCoverage)
class MedicalAidCoverageAdmin(admin.ModelAdmin):
    list_display = ('medical_aid_name', 'coverage_percentage', 'requires_authorization', 'is_active')
    list_filter = ('is_active', 'coverage_percentage')
    search_fields = ('medical_aid_name',)
