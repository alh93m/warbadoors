from django.db import models


class Contact(models.Model):
    """Contact form submissions"""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('spam', 'Spam'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    subject = models.CharField(max_length=255)
    message = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    
    # Admin response
    admin_reply = models.TextField(blank=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    replied_by = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class Newsletter(models.Model):
    """Newsletter subscriptions"""
    
    email = models.EmailField(unique=True)
    is_subscribed = models.BooleanField(default=True)
    
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'
    
    def __str__(self):
        return self.email
