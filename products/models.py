from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    """Product categories"""
    
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Stock doors and products"""
    
    PRODUCT_TYPE_CHOICES = [
        ('stock_door', 'Stock Door'),
        ('custom_door', 'Custom Door'),
        ('accessory', 'Accessory'),
    ]
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
        default='stock_door'
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    
    # Specifications
    material = models.CharField(max_length=100, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)
    weight = models.CharField(max_length=100, blank=True)
    
    # Pricing
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Images
    main_image = models.ImageField(upload_to='products/')
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['product_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """Additional product images"""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"


class DoorDesign(models.Model):
    """Custom door designs"""
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    
    image = models.ImageField(upload_to='designs/')
    thumbnail = models.ImageField(upload_to='designs/thumbnails/')
    
    # Design details
    material = models.CharField(max_length=100, blank=True)
    style = models.CharField(max_length=100, blank=True)
    features = models.TextField(blank=True, help_text="Comma-separated features")
    
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Door Design'
        verbose_name_plural = 'Door Designs'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Color(models.Model):
    """Door colors and finishes"""
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    # Color code
    hex_code = models.CharField(
        max_length=7,
        help_text="Hex color code (e.g., #FF5733)"
    )
    rgb_value = models.CharField(
        max_length=20,
        blank=True,
        help_text="RGB value (e.g., rgb(255, 87, 51))"
    )
    
    # Images
    swatch_image = models.ImageField(upload_to='colors/swatches/')
    preview_image = models.ImageField(
        upload_to='colors/previews/',
        blank=True,
        null=True,
        help_text="Fullscreen preview image"
    )
    
    # Metadata
    finish_type = models.CharField(
        max_length=50,
        choices=[
            ('glossy', 'Glossy'),
            ('matte', 'Matte'),
            ('satin', 'Satin'),
            ('textured', 'Textured'),
        ],
        default='glossy'
    )
    
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class LegacyCategory(models.Model):
    """Legacy catalog category (separate from modern Product Category)."""

    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=300,blank=True,null = True)
    title = models.CharField(max_length=250,null=True,blank=True)
    category = models.ForeignKey(
        LegacyCategory,
        on_delete=models.CASCADE,
        null=True,
    )
    quantity = models.IntegerField(blank=True,null=True)
    discount = models.FloatField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField( max_digits=9, decimal_places=2,blank=True,null=True)
    is_approve = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    width = models.CharField(max_length=30,blank=True,null = True)
    height = models.CharField(max_length=30,blank=True,null = True)
    depth = models.CharField(max_length=30,blank=True,null = True)
    weight = models.CharField(max_length=30,blank=True,null = True)
    quality_checking = models.CharField(max_length=30,blank=True,null = True)
    image = models.ImageField(upload_to='product',blank=True,null=True)
    def __str__(self):
        return self.name