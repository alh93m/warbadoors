from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_id', 'color', 'quantity', 'created_by', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'requested_date')
    search_fields = ('reservation_id', 'contract_number', 'color__name')
    readonly_fields = ('reservation_id', 'created_at', 'updated_at', 'approved_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Reservation Info', {
            'fields': ('reservation_id', 'color', 'quantity', 'contract_number')
        }),
        ('Status', {
            'fields': ('status', 'created_by', 'approved_by')
        }),
        ('Dates', {
            'fields': ('requested_date', 'required_by_date', 'created_at', 'updated_at', 'approved_at')
        }),
        ('Notes', {
            'fields': ('notes', 'rejection_reason')
        }),
    )
