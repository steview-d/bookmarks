from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import PasswordChangeForm


class RegisterAccountForm(UserCreationForm):
    """ extend default form with email field """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterAccountForm, self).__init__(*args, **kwargs)
        # move help_text to a data-attribute so it can be used with
        # tippy.js and displayed in a tooltip
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({
                    'class': 'tippy-help-text',
                    'data-helptext': help_text
                    })


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


class UpdatedPasswordChangeForm(PasswordChangeForm):
    """
    PasswordChangeForm has autofocus set to True for the old_password field
    App profile page contains more than 1 form, so subclassing form to set
    autofocus to False on this field.
    """

    def __init__(self, *args, **kwargs):
        super(UpdatedPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['autofocus'] = False
