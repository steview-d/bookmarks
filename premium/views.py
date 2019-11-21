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
    # add user to premium group
    # premium_group = Group.objects.get(name='Premium')
    # user = User.objects.get(email=request.user.email)
    # user.groups.add(premium_group)

    if request.method == "POST":
        purchase_premium_form = PremiumPurchaseForm(request.POST)
        payment_form = PaymentForm(request.POST)

        # check forms are valid, save if they are
        if purchase_premium_form.is_valid() and payment_form.is_valid():
            purchase_premium = purchase_premium_form.save(commit=False)
            # tidy this up if nothing else needs adding
            # date should be auto added, but check
            # purchase_premium.user = request.user
            print("ORDER VALID")
            purchase_premium.save()

            # no need to build an order, as a one off payment

            # stripe stuff....
            try:
                customer = stripe.Charge.create(
                    amount=premium_cost * 100,
                    currency="GBP",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id']
                )
            except stripe.error.CardError:
                messages.error(request, "Card declined")

            if customer.paid:
                messages.error(request, "You have paid")
                # add user to premium group
                premium_group = Group.objects.get(name='Premium')
                user = User.objects.get(email=request.user.email)
                user.groups.add(premium_group)
                return redirect(reverse('premium'))
            else:
                messages.error(request, "Couldn't take payment")
        else:
            messages.error(request, "Can't take payment with that card")
    else:
        purchase_premium_form = PremiumPurchaseForm()
        payment_form = PaymentForm()

    context = {'purchase_premium_form': purchase_premium_form,
               'payment_form': payment_form,
               'publishable': settings.STRIPE_PUBLISHABLE}
    context = is_premium(request.user, context)

    return render(request, 'premium/premium.html', context)


# install stripe with pip - what else?
