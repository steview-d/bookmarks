from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


# Create your models here.
class Ticket(models.Model):
    user = models.ForeignKey(
        User, default=1, null=False, on_delete=models.CASCADE
    )
    email = models.EmailField(
        max_length=100, null=True
    )
    title = models.CharField(
        max_length=50, null=False, blank=False
    )
    message = models.TextField(
        null=False, blank=False
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
