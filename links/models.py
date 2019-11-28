from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class Collection(models.Model):
    user = models.ForeignKey(
        User, default=1, null=False, on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=30, null=False, blank=False
    )

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    user = models.ForeignKey(
        User, default=1, null=False, on_delete=models.CASCADE
    )
    collection = models.ForeignKey(
        Collection,
        default=1, null=False, blank=False,
        on_delete=models.CASCADE, related_name='bookmarks'
    )
    url = models.TextField(
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
        unique=True, null=False, blank=False
    )
    position_temp = models.PositiveIntegerField(
        null=True, blank=True
    )

    def __str__(self):
        return self.url
