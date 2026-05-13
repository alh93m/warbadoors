from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom user admin configuration"""
    list_display = ('username', 'email', 'get_full_name', 'role', 'is_verified', 'created_at')
    list_filter = ('role', 'is_verified', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'company_name', 'is_verified')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code'),
            'classes': ('collapse',)
        }),
    )
