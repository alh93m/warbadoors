from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from core.models import ScopedBranchModel


class Payment(ScopedBranchModel, models.Model):
    """Payment transactions — single source of truth for money movement."""

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('upayments', 'UPayments'),
        ('card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    PAYMENT_FOR_CHOICES = [
        ('booking', 'Measurement Booking'),
        ('order', 'Product Order'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
    )

    payment_id = models.CharField(max_length=100, unique=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    currency = models.CharField(max_length=3, default='AED')
    payment_for = models.CharField(
        max_length=20,
        choices=PAYMENT_FOR_CHOICES,
        default='booking',
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='upayments',
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
    )

    booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='payments',
    )

    sales_order = models.OneToOneField(
        'shopping.SalesOrder',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='payment',
    )

    upayments_invoice = models.CharField(max_length=255, blank=True)
    upayments_reference = models.CharField(max_length=255, blank=True)

    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    gateway_response = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment_id']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'created_at']),
            GinIndex(fields=['gateway_response'], name='payment_gateway_response_gin'),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(booking__isnull=True) | Q(sales_order__isnull=True),
                name='payment_chk_booking_xor_sales_order',
            ),
        ]

    def __str__(self):
        return f"Payment {self.payment_id} - {self.amount} {self.currency}"

    def clean(self):
        super().clean()
        if self.booking_id and self.sales_order_id:
            raise ValidationError(
                'A payment cannot reference both a booking and a sales order.'
            )
        if self.status == 'completed':
            if self.payment_for == 'booking' and not self.booking_id:
                raise ValidationError(
                    {'booking': 'Completed booking payments must reference a booking.'}
                )
            if self.payment_for == 'order' and not self.sales_order_id:
                raise ValidationError(
                    {
                        'sales_order': (
                            'Completed order payments must reference a sales order.'
                        )
                    }
                )
            if self.payment_for == 'other' and (
                self.booking_id or self.sales_order_id
            ):
                raise ValidationError(
                    'Completed general payments cannot reference bookings or orders.'
                )


class PaymentLog(models.Model):
    """Audit trail for payment API calls (never delete parent Payment rows casually)."""

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='logs',
    )

    action = models.CharField(
        max_length=50,
        choices=[
            ('initiated', 'Payment Initiated'),
            ('verified', 'Payment Verified'),
            ('webhook', 'Webhook Received'),
            ('refund_requested', 'Refund Requested'),
            ('error', 'Error'),
        ],
    )

    request_data = models.JSONField(blank=True, null=True)
    response_data = models.JSONField(blank=True, null=True)
    status_code = models.IntegerField(blank=True, null=True)
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Payment Log'
        verbose_name_plural = 'Payment Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment', 'created_at']),
        ]

    def __str__(self):
        return f"{self.payment.payment_id} - {self.action}"
