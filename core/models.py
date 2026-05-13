from django.db import models


class CompanyInfo(models.Model):
    """Company configuration and branding"""
    
    name = models.CharField(max_length=255, default='Warba Doors')
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    
    # Contact info
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    
    # Address
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    # Social media
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    whatsapp_link = models.URLField(blank=True, null=True)
    
    # Payment
    upayments_public_key = models.CharField(max_length=255, blank=True)
    upayments_private_key = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Company Info'
        verbose_name_plural = 'Company Info'
    
    def __str__(self):
        return self.name


class Branch(models.Model):
    """Company branches/locations"""
    
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ScopedBranchModel(models.Model):
    """Optional branch scope for future multi-company / SaaS expansion."""

    scope_branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        db_index=True,
        help_text='Optional operating branch; use for per-tenant data partitioning later.',
    )

    class Meta:
        abstract = True


class FAQ(models.Model):
    """Frequently Asked Questions"""
    
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('booking', 'Booking'),
            ('products', 'Products'),
            ('payment', 'Payment'),
            ('shipping', 'Shipping'),
            ('general', 'General'),
        ],
        default='general'
    )
    
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['order']
    
    def __str__(self):
        return self.question[:50]
