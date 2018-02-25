from django.contrib import admin

from .models import Trade, Contract

class TradeAdmin(admin.ModelAdmin):
    list_display = ('address', 'contract', 'date_creation', 'price', 'is_the_cheapest')
    list_filter = ['date_creation']

class ContractAdmin(admin.ModelAdmin):
    list_display = ('address', 'name', 'ticker', 'date_creation')
    list_filter = ['date_creation']
    search_fields = ['name']
    
admin.site.register(Trade, TradeAdmin)
admin.site.register(Contract, ContractAdmin)