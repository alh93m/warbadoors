from django.contrib import admin
from .models import Payment, PaymentLog


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'amount', 'currency', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'payment_for', 'created_at')
    search_fields = ('payment_id', 'user__email', 'transaction_id')
    readonly_fields = (
        'payment_id',
        'created_at',
        'updated_at',
        'gateway_response',
    )
    date_hierarchy = 'created_at'


@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ('payment', 'action', 'status_code', 'created_at')
    list_filter = ('action', 'status_code', 'created_at')
    search_fields = ('payment__payment_id',)
    readonly_fields = (
        'created_at',
        'request_data',
        'response_data',
    )
    date_hierarchy = 'created_at'
