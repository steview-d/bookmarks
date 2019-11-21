from django import forms

from .models import PurchasePremium


class PurchasePremiumForm(forms.ModelForm):

    class Meta:
        model = PurchasePremium
        fields = ['full_name',
                  'street_address1',
                  'street_address2',
                  'town_city',
                  'county',
                  'postcode',
                  'country']


class PaymentForm(forms.Form):

    MONTH_CHOICES = [(i, i) for i in range(1, 13)]
    YEAR_CHOICES = [(i, i) for i in range(2019, 2030)]

    credit_card_number = forms.CharField(
        label='Credit Card Number', required=False
    )
    cvv = forms.CharField(
        label='Security Code (CVV)', required=False
    )
    expiry_month = forms.ChoiceField(
        label='Expiry Month', choices=MONTH_CHOICES, required=False
    )
    expiry_year = forms.ChoiceField(
        label='Expiry Year', choices=YEAR_CHOICES, required=False
    )
    stripe_id = forms.CharField(
        widget=forms.HiddenInput
    )
