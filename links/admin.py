from django import forms
from django.contrib import admin

from .models import Bookmark, Collection, Page


# Register your models here.
class PageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'num_of_columns',
        'user',
        'position'
    )


class CollectionAdmin(admin.ModelAdmin):

    list_display = (
        'collection_name',
        'position',
        'page',
        'user',
    )


class BookmarkAdmin(admin.ModelAdmin):

    # force admin form to use Textarea to display description
    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'description': forms.Textarea(
            attrs={'cols': '50', 'rows': '5'})}
        return super().get_form(request, obj, **kwargs)

    readonly_fields = ['id', 'added', 'updated']

    fieldsets = [
        ('Bookmark', {'fields': ['url', 'title', 'description']}),
        ('Grouping', {'fields': ['collection', 'position']}),
        ('User', {'fields': ['user', 'added', 'updated']}),

    ]

    list_display = (
        'url',
        'title',
        'collection',
        'user',
        'added',
    )

    ordering = ['-added']


admin.site.register(Page, PageAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
