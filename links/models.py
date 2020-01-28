from django.conf import settings
from django.core.files.storage import default_storage
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from PIL import Image

User = settings.AUTH_USER_MODEL


class Page(models.Model):
    """
    A page is a single view for the user than contains a number of collections.
    Initially, only 1 page per user, and can be used to store settings for
    collections.
    """
    user = models.ForeignKey(
        User, default=1, null=False, on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=30, null=False, blank=False
    )
    position = models.PositiveIntegerField(
        null=False, blank=False
    )
    position_temp = models.PositiveIntegerField(
        null=True, blank=True
    )
    num_of_columns = models.PositiveIntegerField(
        default=4, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    collection_order_2 = models.TextField(
        null=True, blank=True
    )
    collection_order_3 = models.TextField(
        null=True, blank=True
    )
    collection_order_4 = models.TextField(
        null=True, blank=True
    )
    collection_order_5 = models.TextField(
        null=True, blank=True
    )

    class Meta:
        unique_together = [['position', 'user'], ['name', 'user']]

    def __str__(self):
        return self.name


class Collection(models.Model):
    user = models.ForeignKey(
        User, default=1, null=False, on_delete=models.CASCADE
    )
    page = models.ForeignKey(
        Page, default=1, null=False, on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=30, null=False, blank=False
    )
    position = models.PositiveIntegerField(
        null=False, blank=False
    )
    position_temp = models.PositiveIntegerField(
        null=True, blank=True
    )
    display_mode = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(3)],
        null=False, blank=True
    )
    sort_order = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(6)],
        null=False, blank=True
    )

    class Meta:
        unique_together = [['name', 'user', 'page'],
                           ['position', 'name', 'page', 'user']]

    def __str__(self):
        return self.name

    def collection_name(self):
        return self.name

    collection_name.short_description = "Collection Name"


def icon_location(instance, filename):
    return "icons/{}/{}".format(instance.user.username.lower(), filename)


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
    icon = models.ImageField(
        upload_to=icon_location, null=True, blank=True
    )
    added = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    position = models.PositiveIntegerField(
        null=False, blank=True
    )
    position_temp = models.PositiveIntegerField(
        null=True, blank=True
    )

    class Meta:
        unique_together = ['collection', 'position']

    def __str__(self):
        return self.url

    def bookmark_page(self):
        page = Page.objects.get(
            collection=self.collection
        )
        return page.name

    def save(self, *args, **kwargs):
        # handle images on save
        super(Bookmark, self).save(*args, **kwargs)
        if self.icon:
            im = Image.open(self.icon)
            px_size = 128
            # resize image if too large
            if im.height > px_size or im.width > px_size:
                new_im = im.resize((px_size, px_size))
                tmp = default_storage.open(self.icon.name, 'wb')
                new_im.save(tmp)
                tmp.close()
                im.close()


class MoveBookmark(models.Model):
    dest_page = models.ForeignKey(
        Page,
        default=1, null=False, blank=False, on_delete=models.CASCADE
    )
    dest_collection = models.ForeignKey(
        Collection,
        default=1, null=False, blank=False, on_delete=models.CASCADE
    )
