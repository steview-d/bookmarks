from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class Ticket(models.Model):

    STATUS_CHOICE = (
        ('OPEN', 'OPEN'),
        ('CLOSED', 'CLOSED'),
    )

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
    admin_comments = models.TextField(
        null=True, blank=True
    )
    status = models.CharField(
        max_length=6, choices=STATUS_CHOICE, default="OPEN"
    )

    def __str__(self):
        return self.title

    def admin_commented(self):
        return True if self.admin_comments else False

    admin_commented.boolean = True
    admin_commented.short_description = "Admin Comment(s)?"
