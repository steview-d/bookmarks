from django.contrib import admin

from .models import PremiumPurchase


class PremiumPurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date', 'user_email')

    def user_email(self, obj):
        return obj.user.email

    fieldsets = [
        ('Purchase Information',
            {'fields': ['user',
                        'payment_amount',
                        'date',
                        'id']}),
        ('User Details',
            {'fields': ['user_email',
                        'full_name',
                        'postcode']}),
    ]

    list_display = (
        'id', 'user', 'user_email', "payment_amount", 'date'
    )


admin.site.register(PremiumPurchase, PremiumPurchaseAdmin)
