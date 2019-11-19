from django.contrib import admin

# Register your models here.
from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

    fieldsets = [
        ('Overview', {'fields': ['id', 'date_created', 'user', 'email']}),
        ('Ticket Detail', {'fields': ['title', 'message']}),
        ('Admin', {'fields': ['admin_comments']}),

    ]

    list_display = ('id', 'user', 'title', 'date_created', 'admin_commented')
    list_filter = ['date_created']


admin.site.register(Ticket, TicketAdmin)
