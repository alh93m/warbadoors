from django.contrib import admin
from .models import ColorStock, StockAdjustment, StockLog


@admin.register(ColorStock)
class ColorStockAdmin(admin.ModelAdmin):
    list_display = ('color', 'total_quantity', 'reserved_quantity', 'available_quantity', 'needs_reorder')
    list_filter = ('needs_reorder',)
    search_fields = ('color__name',)
    readonly_fields = ('available_quantity', 'last_updated')


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('color_stock', 'adjustment_type', 'quantity', 'adjusted_by', 'adjusted_at')
    list_filter = ('adjustment_type', 'adjusted_at')
    search_fields = ('color_stock__color__name', 'reference_id')
    readonly_fields = ('adjusted_at',)
    date_hierarchy = 'adjusted_at'


@admin.register(StockLog)
class StockLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_colors', 'total_stock', 'colors_needing_reorder')
    list_filter = ('date',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'date'
