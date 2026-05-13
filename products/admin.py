from django.contrib import admin
from .models import Category, Product, ProductImage, DoorDesign, Color, LegacyCategory


@admin.register(LegacyCategory)
class LegacyCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'category', 'price', 'is_active', 'is_featured')
    list_filter = ('product_type', 'is_active', 'is_featured', 'category')
    search_fields = ('name', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(DoorDesign)
class DoorDesignAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'is_featured', 'order')
    list_filter = ('is_active', 'is_featured')
    search_fields = ('name', 'style')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code', 'finish_type', 'is_active', 'is_featured', 'order')
    list_filter = ('is_active', 'is_featured', 'finish_type')
    search_fields = ('name', 'hex_code')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')