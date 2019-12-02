from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class Page(models.Model):
    """
    A page is a single view for the user than contains a number of collections.
    Initially, only 1 page per user, and can be used to store settings for
    collections.
    Eventually will expand app to allow multiple pages.
    """
    user = models.ForeignKey(
        User, default=1, null=False, on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=30, null=False, blank=False
    )
    public = models.BooleanField(
        default=False
    )
    position = models.PositiveIntegerField(
        null=False, blank=False
    )

    def __str__(self):
        return self.name


class Collection(models.Model):
    """
    column & position defaults to 1000 so on creation, they are placed
    at end of list. - removed, for now

    *** Later on need to add code that on saving, sorts columns & positions
    to create a nice 1, 2, 3, 4 order, and so on.
    look into default save() method added to model I've seen used elsewhere?

    """
    user = models.ForeignKey(
        User, default=1, null=False, on_delete=models.CASCADE
    )
    page = models.ForeignKey(
        Page, default=1, null=False, on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=30, null=False, blank=False
    )
    column = models.PositiveIntegerField(
        null=False, blank=False
    )
    position = models.PositiveIntegerField(
        null=False, blank=False
    )
    position_temp = models.PositiveIntegerField(
        null=True, blank=True
    )

    class Meta:
        unique_together = ['name', 'user']
        unique_together = ['position', 'column', 'user']

    def __str__(self):
        return self.name

    def collection_name(self):
        return self.name

    collection_name.short_description = "Collection Name"


class Bookmark(models.Model):
    user = models.ForeignKey(
        User, default=1, null=False, on_delete=models.CASCADE
    )
    collection = models.ForeignKey(
        Collection,
        default=1, null=False, blank=False,
        on_delete=models.CASCADE, related_name='bookmarks'
    )
    url = models.URLField(
        null=False, blank=False
    )
    title = models.CharField(
        max_length=100, null=False, blank=False
    )
    description = models.CharField(
        max_length=500, null=True, blank=True
    )
    added = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    position = models.PositiveIntegerField(
        null=False, blank=False
    )
    position_temp = models.PositiveIntegerField(
        null=True, blank=True
    )

    class Meta:
        unique_together = ['collection', 'position']

    def __str__(self):
        return self.url
