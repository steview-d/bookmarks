from django.contrib import admin

from .models import Ticket


def close_tickets(modeladmin, request, queryset):
    for ticket in queryset:
        ticket.status = "CLOSED"
        ticket.save()


def open_tickets(modeladmin, request, queryset):
    for ticket in queryset:
        ticket.status = "OPEN"
        ticket.save()


close_tickets.short_description = "Close selected tickets"
open_tickets.short_description = "Open selected tickets"


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

    actions = [close_tickets, open_tickets]


admin.site.register(Ticket, TicketAdmin)
