from django.contrib import admin
from .models import CompanyInfo, Branch, FAQ


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone', 'is_active')
    list_filter = ('is_active', 'city')
    search_fields = ('name', 'city')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'is_active', 'order')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')
