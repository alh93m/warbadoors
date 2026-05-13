from django.contrib import admin
from .models import Booking, BookingTimeslot


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'customer', 'status', 'preferred_date', 'created_at')
    list_filter = ('status', 'created_at', 'preferred_date')
    search_fields = ('booking_id', 'customer__email', 'customer__username')
    readonly_fields = ('booking_id', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Booking Info', {
            'fields': ('booking_id', 'customer', 'status')
        }),
        ('Project Details', {
            'fields': ('project_name', 'project_description', 'number_of_doors', 'services')
        }),
        ('Location', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Scheduling', {
            'fields': ('preferred_date', 'preferred_time_slot', 'scheduled_date', 'completed_date')
        }),
        ('Contact Information', {
            'fields': ('contact_phone', 'contact_email', 'special_requirements')
        }),
        ('Payment & Amount', {
            'fields': ('booking_amount',)
        }),
        ('Admin Notes', {
            'fields': ('assigned_technician', 'notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BookingTimeslot)
class BookingTimeslotAdmin(admin.ModelAdmin):
    list_display = ('date', 'time_slot', 'current_bookings', 'max_bookings', 'is_available')
    list_filter = ('date', 'time_slot', 'is_available')
    date_hierarchy = 'date'