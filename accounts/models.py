from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with additional fields for Warba Doors.
    Supports multiple roles: customer, admin, inventory_manager, sales_rep
    """
    
    # Role choices
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Administrator'),
        ('inventory_manager', 'Inventory Manager'),
        ('sales_rep', 'Sales Representative'),
    ]
    
    # Profile fields
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer',
        help_text="User role determines access permissions"
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="User phone number"
    )
    
    address = models.TextField(
        blank=True,
        null=True,
        help_text="Delivery/business address"
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    
    state = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    
    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="For B2B customers"
    )
    
    is_verified = models.BooleanField(
        default=False,
        help_text="Email/Phone verification status"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    def is_customer(self):
        return self.role == 'customer'
    
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
    
    def is_inventory_manager(self):
        return self.role == 'inventory_manager'
    
    def is_sales_rep(self):
        return self.role == 'sales_rep'
