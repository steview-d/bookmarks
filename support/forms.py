from django import forms
from .models import Ticket
# from django.contrib.auth.models import User


class SupportRequestForm(forms.ModelForm):
    """ user fills in this form when requesting support """

    class Meta:
        model = Ticket
        fields = ['title', 'message']
