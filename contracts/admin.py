from django.contrib import admin
from .models import Contract, ContractTemplate


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'user', 'contract_type', 'status', 'amount', 'contract_date')
    list_filter = ('contract_type', 'status', 'contract_date')
    search_fields = ('contract_number', 'user__email')
    readonly_fields = ('contract_number', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(ContractTemplate)
class ContractTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'contract_type', 'is_active')
    list_filter = ('contract_type', 'is_active')
    search_fields = ('name',)
