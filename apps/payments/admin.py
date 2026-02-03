from django.contrib import admin
from apps.payments.models import Payment, PaymentShortfall

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'status', 'service_charge', 'patient_co_payment', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('appointment__patient__first_name', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at', 'processed_at')


@admin.register(PaymentShortfall)
class PaymentShortfallAdmin(admin.ModelAdmin):
    list_display = ('payment', 'shortfall_amount', 'patient_notified', 'created_at')
    list_filter = ('patient_notified', 'created_at')
    readonly_fields = ('created_at',)
