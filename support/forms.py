from django import forms
from .models import Ticket


class SupportRequestForm(forms.ModelForm):
    """ user fills in this form when requesting support """

    class Meta:
        model = Ticket
        fields = ['title', 'message']
