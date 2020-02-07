from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Contact form for a non-registered/logged in user to
    communicate with site admin
    """

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
