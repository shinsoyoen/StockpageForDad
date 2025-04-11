from django.contrib import admin
from .models import TransactionHistory

@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('trade_id', 'category', 'trans_date', 'quantity', 'price') 
    list_filter = ('category', 'trans_date')                                              
    search_fields = ('memo',)
    ordering = ('-trans_date',)                                                          
    readonly_fields = ('trade_id',)

    fieldsets = (
        (None, {
            'fields': ('category', 'trans_date', 'quantity', 'price', 'memo')
        }),
    )


