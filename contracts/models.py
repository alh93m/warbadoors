from django.db import models
from django.conf import settings


class Contract(models.Model):
    """Automated contracts generated after payment"""
    
    CONTRACT_STATUS_CHOICES = [
        ('generated', 'Generated'),
        ('sent', 'Sent to Customer'),
        ('signed', 'Signed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    CONTRACT_TYPE_CHOICES = [
        ('booking', 'Booking Contract'),
        ('order', 'Purchase Order'),
        ('service', 'Service Agreement'),
    ]
    
    # Contract identification
    contract_number = models.CharField(max_length=50, unique=True)
    contract_type = models.CharField(
        max_length=20,
        choices=CONTRACT_TYPE_CHOICES,
        default='booking'
    )
    
    # References
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contracts'
    )
    
    booking = models.OneToOneField(
        'bookings.Booking',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contract'
    )
    
    payment = models.OneToOneField(
        'payments.Payment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contract'
    )
    
    # Contract details
    subject = models.CharField(max_length=255)
    description = models.TextField()
    
    # Financial
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='AED')
    
    # Dates
    contract_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    # Terms
    terms_and_conditions = models.TextField()
    special_terms = models.TextField(blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=CONTRACT_STATUS_CHOICES,
        default='generated'
    )
    
    # Documents
    pdf_file = models.FileField(
        upload_to='contracts/pdfs/',
        blank=True,
        null=True,
        help_text="Generated PDF contract"
    )
    
    # Tracking
    sent_to_email = models.EmailField(blank=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    viewed_at = models.DateTimeField(blank=True, null=True)
    signed_at = models.DateTimeField(blank=True, null=True)
    
    # Additional
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['contract_number']),
            models.Index(fields=['user']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Contract {self.contract_number}"
    
    def save(self, *args, **kwargs):
        if not self.contract_number:
            from datetime import datetime
            self.contract_number = f"CT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)


class ContractTemplate(models.Model):
    """Templates for contract generation"""
    
    name = models.CharField(max_length=255)
    contract_type = models.CharField(
        max_length=20,
        choices=[
            ('booking', 'Booking Contract'),
            ('order', 'Purchase Order'),
            ('service', 'Service Agreement'),
        ]
    )
    
    template_content = models.TextField(
        help_text="HTML template with {{variable}} placeholders"
    )
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Contract Template'
        verbose_name_plural = 'Contract Templates'
    
    def __str__(self):
        return self.name
