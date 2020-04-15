from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


# Create your models here.
class PremiumPurchase(models.Model):
    """ stores details of each user upgrading to Premium"""

    user = models.OneToOneField(
        User, default=1, null=False, on_delete=models.CASCADE
    )
    full_name = models.CharField(
        max_length=50, blank=False
    )
    postcode = models.CharField(
        max_length=12, blank=False
    )
    date = models.DateTimeField(
        auto_now_add=True
    )
    payment_amount = models.IntegerField(
        default=0, blank=False, null=True
    )

    def __str__(self):
        return f"{self.id}-{self.user}"
