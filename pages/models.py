from django.db import models


class Contact(models.Model):
    """
    ...
    """
    name = models.CharField(
        max_length=30, null=False, blank=False
    )
    email = models.EmailField(
        max_length=254, null=False, blank=False
    )
    message = models.CharField(
        max_length=500, null=False, blank=False
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    actioned = models.BooleanField(
        default=False, blank=True
    )

    def __str__(self):
        return self.email

    def is_actioned(self):
        return True if self.actioned else False

    is_actioned.short_description = "Actioned?"
