from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):

    readonly_fields = ['date_created']

    fieldsets = [
        ('Message Detail', {'fields': ['email', 'name', 'message']}),
        ('Admin', {'fields': ['date_created', 'actioned']}),
    ]

    list_display = (
        'email', 'name', 'message', 'date_created', 'actioned'
    )

    list_filter = ['actioned', 'date_created']


admin.site.register(Contact, ContactAdmin)
