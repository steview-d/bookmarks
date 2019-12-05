from django import forms

from .models import Page


class AddNewPageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ['name', 'num_of_columns']
