from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Reservation(models.Model):
    """Color reservations by sales representatives"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    # Reservation details
    reservation_id = models.CharField(max_length=50, unique=True)
    
    # Sales rep who made the reservation
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'sales_rep'},
        related_name='reservations_created'
    )
    
    # Color being reserved
    color = models.ForeignKey(
        'products.Color',
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    
    # Reservation quantity
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    
    # Contract reference
    contract_number = models.CharField(
        max_length=50,
        help_text="Customer contract number"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Approval
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'inventory_manager'},
        related_name='reservations_approved'
    )
    
    # Notes
    notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Dates
    requested_date = models.DateField()
    required_by_date = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reservation_id']),
            models.Index(fields=['status']),
            models.Index(fields=['created_by']),
            models.Index(fields=['color', 'status']),
            models.Index(fields=['contract_number']),
        ]
    
    def __str__(self):
        return f"Reservation {self.reservation_id}"
    
    def save(self, *args, **kwargs):
        if not self.reservation_id:
            from datetime import datetime
            self.reservation_id = f"RS{datetime.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)
