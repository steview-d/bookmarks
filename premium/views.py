from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render, reverse
import stripe

from .forms import PremiumPurchaseForm, PaymentForm
from .utils import is_premium


stripe.api_key = settings.STRIPE_SECRET

# set the current price a user will pay for premium access
premium_cost = 20

# Create your views here.
@login_required
def premium(request):
    if request.method == "POST":
        purchase_premium_form = PremiumPurchaseForm(request.POST)
        payment_form = PaymentForm(request.POST)

        # check forms are valid, save if they are
        if purchase_premium_form.is_valid() and payment_form.is_valid():
            # stripe
            try:
                customer = stripe.Charge.create(
                    amount=premium_cost * 100,
                    currency="GBP",
                    description=(request.user.email + " | " +
                                 purchase_premium_form.cleaned_data
                                 ['postcode']),
                    card=payment_form.cleaned_data['stripe_id']
                )
            except stripe.error.CardError:
                messages.error(
                    request, "Sorry, your card has been declined. \
                        You should contact your card issuer.")

            if customer.paid:
                messages.success(
                    request, f"Your payment of £{premium_cost} \
                        has been recieved. Thank you.")
                # update and save form
                purchase_premium = purchase_premium_form.save(commit=False)
                purchase_premium.user = request.user
                purchase_premium.payment_amount = premium_cost
                purchase_premium.save()
                # add user to premium group
                premium_group = Group.objects.get(name='Premium')
                user = User.objects.get(email=request.user.email)
                user.groups.add(premium_group)
                return redirect(reverse('premium'))
            else:
                messages.error(
                    request, "Sorry, your payment could not be taken. \
                        Please try again, or use a different card")
        else:
            messages.error(
                request, "Sorry, your payment could not be taken. \
                    Please use a different card")
    else:
        purchase_premium_form = PremiumPurchaseForm()
        payment_form = PaymentForm()

    context = {'purchase_premium_form': purchase_premium_form,
               'payment_form': payment_form,
               'publishable': settings.STRIPE_PUBLISHABLE}
    context = is_premium(request.user, context)

    return render(request, 'premium/premium.html', context)
