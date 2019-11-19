from django.contrib import admin

# Register your models here.
from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date_created')

    fieldsets = [
        ('Overview', {'fields': ['id', 'date_created', 'user', 'email']}),
        ('Ticket Detail', {'fields': ['title', 'message']}),
        ('Admin', {'fields': ['admin_comments', 'status']}),

    ]

    list_display = (
        'id',
        'user',
        'title',
        'date_created',
        'admin_commented',
        'status')
    list_filter = ['status', 'date_created']


admin.site.register(Ticket, TicketAdmin)
