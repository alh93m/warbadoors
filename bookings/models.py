from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

from core.models import ScopedBranchModel


class Booking(ScopedBranchModel, models.Model):
    """Measurement booking requests"""
    
    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('measurement_scheduled', 'Measurement Scheduled'),
        ('measurement_completed', 'Measurement Completed'),
        ('quote_sent', 'Quote Sent'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    # Customer info
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    
    # Booking details
    booking_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=30,
        choices=BOOKING_STATUS_CHOICES,
        default='pending'
    )
    
    # Project information
    project_name = models.CharField(max_length=255, blank=True)
    project_description = models.TextField(blank=True)
    number_of_doors = models.IntegerField(validators=[MinValueValidator(1)])
    
    # Location
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Preferred dates
    preferred_date = models.DateField()
    preferred_time_slot = models.CharField(
        max_length=50,
        choices=[
            ('morning', 'Morning (8AM - 12PM)'),
            ('afternoon', 'Afternoon (12PM - 4PM)'),
            ('evening', 'Evening (4PM - 8PM)'),
        ]
    )
    
    # Services
    services = models.TextField(
        blank=True,
        help_text="Comma-separated services (e.g., measurement, consultation, design)"
    )
    
    # Additional info
    special_requirements = models.TextField(blank=True)
    
    # Booking amount
    booking_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Measurement service fee"
    )
    
    # Tracking
    assigned_technician = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheduled_date = models.DateTimeField(blank=True, null=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['booking_id']),
            models.Index(fields=['customer']),
            models.Index(fields=['status']),
            models.Index(fields=['preferred_date']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Booking {self.booking_id} - {self.customer.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            from datetime import datetime
            self.booking_id = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)


class BookingTimeslot(models.Model):
    """Available measurement booking timeslots"""
    
    date = models.DateField()
    time_slot = models.CharField(
        max_length=50,
        choices=[
            ('morning', 'Morning (8AM - 12PM)'),
            ('afternoon', 'Afternoon (12PM - 4PM)'),
            ('evening', 'Evening (4PM - 8PM)'),
        ]
    )
    
    max_bookings = models.IntegerField(default=5)
    current_bookings = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Booking Timeslot'
        verbose_name_plural = 'Booking Timeslots'
        unique_together = ['date', 'time_slot']
        ordering = ['date', 'time_slot']
    
    def __str__(self):
        return f"{self.date} - {self.get_time_slot_display()}"
    
    def is_slot_available(self):
        return self.is_available and self.current_bookings < self.max_bookings
