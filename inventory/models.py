from django.db import models
from django.db.models import F, Q
from django.core.validators import MinValueValidator


class ColorStock(models.Model):
    """Color inventory stock tracking"""

    color = models.OneToOneField(
        'products.Color',
        on_delete=models.CASCADE,
        related_name='stock',
    )

    total_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    reserved_quantity = models.IntegerField(
        validators=[MinValueValidator(0)], default=0
    )
    damaged_quantity = models.IntegerField(
        validators=[MinValueValidator(0)], default=0
    )

    available_quantity = models.IntegerField(
        validators=[MinValueValidator(0)], default=0
    )

    min_stock_level = models.IntegerField(validators=[MinValueValidator(0)], default=10)
    reorder_quantity = models.IntegerField(validators=[MinValueValidator(1)], default=50)

    needs_reorder = models.BooleanField(default=False)

    last_updated = models.DateTimeField(auto_now=True)
    last_restock_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Color Stock'
        verbose_name_plural = 'Color Stock'
        indexes = [
            models.Index(fields=['needs_reorder', 'available_quantity']),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(total_quantity__gte=0)
                & Q(reserved_quantity__gte=0)
                & Q(damaged_quantity__gte=0)
                & Q(available_quantity__gte=0),
                name='inventory_colorstock_nonneg_components',
            ),
            models.CheckConstraint(
                check=Q(total_quantity__gte=F('reserved_quantity') + F('damaged_quantity')),
                name='inventory_colorstock_reserves_lte_total',
            ),
        ]

    def __str__(self):
        return f"{self.color.name} - Stock"

    def calculate_available(self):
        """Derive available from total, reserved, and damaged."""
        self.available_quantity = (
            self.total_quantity - self.reserved_quantity - self.damaged_quantity
        )
        self.needs_reorder = self.available_quantity <= self.min_stock_level
        return self.available_quantity

    def save(self, *args, **kwargs):
        self.calculate_available()
        super().save(*args, **kwargs)


class StockAdjustment(models.Model):
    """Track stock adjustments and movements"""

    ADJUSTMENT_TYPE_CHOICES = [
        ('restock', 'Restock'),
        ('damage', 'Damaged'),
        ('adjustment', 'Adjustment'),
        ('loss', 'Loss'),
        ('return', 'Return'),
    ]

    color_stock = models.ForeignKey(
        ColorStock,
        on_delete=models.CASCADE,
        related_name='adjustments',
    )

    adjustment_type = models.CharField(max_length=20, choices=ADJUSTMENT_TYPE_CHOICES)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    reason = models.TextField(blank=True)
    reference_id = models.CharField(max_length=100, blank=True)

    adjusted_by = models.CharField(max_length=255)
    adjusted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Stock Adjustment'
        verbose_name_plural = 'Stock Adjustments'
        ordering = ['-adjusted_at']
        indexes = [
            models.Index(fields=['color_stock', 'adjusted_at']),
        ]

    def __str__(self):
        return f"{self.color_stock.color.name} - {self.adjustment_type}"


class StockLog(models.Model):
    """Daily stock report and audit trail"""

    date = models.DateField(unique=True)
    total_colors = models.IntegerField()
    total_stock = models.IntegerField()
    total_reserved = models.IntegerField()
    colors_needing_reorder = models.IntegerField()

    notes = models.TextField(blank=True)

    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Stock Log'
        verbose_name_plural = 'Stock Logs'
        ordering = ['-date']

    def __str__(self):
        return f"Stock Report - {self.date}"
