from django.contrib import admin

from .models import PremiumPurchase


# Register your models here.
class PremiumPurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date')

    fieldsets = [
        ('Purchase Information',
            {'fields': ['user',
                        'full_name',
                        'payment_amount',
                        'date',
                        'id']}),
        ('Address Details',
            {'fields': ['street_address1',
                        'street_address2',
                        'town_city',
                        'county',
                        'postcode',
                        'country']}),
    ]

    list_display = (
        'id', 'user', "payment_amount", 'date'
    )

    # add country filter so can see at a glance where paying members are from
    list_filter = ['country']


admin.site.register(PremiumPurchase, PremiumPurchaseAdmin)
