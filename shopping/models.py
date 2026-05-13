from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from products.models import Product
from core.models import ScopedBranchModel


class Cart(models.Model):
    """Legacy cart line (one row per user + product; matches existing shopping views)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart_lines',
    )
    product = models.ForeignKey(
        'products.Products',
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    is_parchased = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Cart Line'
        verbose_name_plural = 'Cart Lines'
        indexes = [
            models.Index(fields=['user', 'is_parchased']),
            models.Index(fields=['user', 'product', 'is_parchased']),
        ]

    def __str__(self):
        return f"{self.quantity}x {self.product}"

    def get_total(self):
        if self.product_id and self.product.price is not None:
            return float(self.product.price) * self.quantity
        return 0.0

    def get_discount(self):
        if not self.product_id or self.product.discount is None:
            return 0.0
        try:
            d = float(self.product.discount)
        except (TypeError, ValueError):
            return 0.0
        line = float(self.product.price or 0) * self.quantity
        if 0 <= d <= 100:
            return line * (d / 100.0)
        return min(d, line)


class SalesOrder(ScopedBranchModel):
    """Paid / tracked product orders (integrates with payments.Payment)."""

    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    order_number = models.CharField(max_length=50, unique=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sales_orders',
    )

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending',
    )

    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_phone = models.CharField(max_length=20)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    tracking_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Sales Order'
        verbose_name_plural = 'Sales Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Order {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            from datetime import datetime

            self.order_number = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Line items for a SalesOrder (catalog Product)."""

    order = models.ForeignKey(
        SalesOrder,
        on_delete=models.CASCADE,
        related_name='items',
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
    )

    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        indexes = [
            models.Index(fields=['order', 'product']),
        ]

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

    def get_subtotal(self):
        return self.product_price * self.quantity


class Order(models.Model):
    """Legacy checkout order (open basket until checkout completes)."""

    PAYMENT_METHOD = (
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Card', 'Card'),
        ('Bkash', 'Bkash'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )
    order_products = models.ManyToManyField(Cart)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    payment_id = models.CharField(max_length=300, blank=True, null=True)
    order_id = models.CharField(max_length=300, blank=True, null=True)
    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD,
        default='Cash on Delivery',
    )

    def get_totals(self):
        total = 0
        for order_product in self.order_products.all():
            total += float(order_product.get_total())
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} billing address"

    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]
        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True

    class Meta:
        verbose_name_plural = 'Billing Addresses'


class whitelist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.ForeignKey(
        'products.Products',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    products = models.IntegerField(blank=True, null=True)
