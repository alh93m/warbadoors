from django.contrib import admin
from .models import Contact, Newsletter


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_subscribed', 'subscribed_at')
    list_filter = ('is_subscribed', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)
