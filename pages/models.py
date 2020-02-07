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

    class Meta:
        def __str__(self):
            return self.email
