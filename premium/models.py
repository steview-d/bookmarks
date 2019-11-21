from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


# Create your models here.
class PurchasePremium(models.Model):
    user = models.OneToOneField(
        User, default=1, null=False, on_delete=models.CASCADE
    )
    full_name = models.CharField(
        max_length=50, blank=False
    )
    street_address1 = models.CharField(
        max_length=40, blank=False
    )
    street_address2 = models.CharField(
        max_length=40, blank=True
    )
    town_city = models.CharField(
        max_length=40, blank=False
    )
    county = models.CharField(
        max_length=40, blank=False
    )
    postcode = models.CharField(
        max_length=12, blank=False
    )
    country = models.CharField(
        max_length=40, blank=False
    )
    date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.id}-{self.user}"
