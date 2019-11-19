from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterAccountForm(UserCreationForm):
    """ extend default form with email field """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUserEmailForm(forms.ModelForm):
    """ form to allow users to change their email address """
    email = forms.CharField(
        widget=forms.EmailInput(),
        max_length=100,
        required=True,
        label="New Email Address"
    )

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        """ check the email address is unique """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError(
                u'This email address already exists, please choose another')
        return email


class SupportRequestForm(forms.Form):
    """ user fills in this form when requesting support """
    username = forms.CharField(
        min_length=4,
        max_length=50,
        required=True,
        label="Username"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(),
        max_length=100,
        required=True,
        label="Email Address"
    )
    title = forms.CharField(
        max_length=50,
        required=True,
        label="Title"
    )
    message = forms.CharField(
        widget=forms.Textarea(),
        required=True,
        label="Message"
    )

    class Meta:
        fields = ['username', 'email', 'title', 'message']

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     return username
