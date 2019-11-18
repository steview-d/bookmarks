from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterAccountForm(UserCreationForm):
    """ extend default form with email field """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UpdateUserEmailForm(forms.ModelForm):
    """ form to allow change their email address """
    email = forms.CharField(
        widget=forms.EmailInput(),
        max_length=100,
        required=True,
        label="New Email Address"
    )

    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self):
        """ check the email address is unique """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError(
                u'This email address already exists, please choose another')
        return email
