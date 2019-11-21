from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render

from .forms import PurchasePremiumForm, PaymentForm
from .utils import is_premium


stripe_api_key = settings.STRIPE_SECRET

# Create your views here.
@login_required
def premium(request):
    # add user to premium group
    # premium_group = Group.objects.get(name='Premium')
    # user = User.objects.get(email=request.user.email)
    # user.groups.add(premium_group)

    if request.method == "POST":
        purchase_premium_form = PurchasePremiumForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if purchase_premium_form.is_valid() and payment_form.is_valid():
            # purchase_premium = purchase_premium_form.save(commit=False)
            # purchase_premium.user = request.user
            print("JJKJKJKJKJK")
            # purchase_premium.save()
        else:
            print("NOT VALID!!!")

    purchase_premium_form = PurchasePremiumForm()
    payment_form = PaymentForm()

    context = {'purchase_premium_form': purchase_premium_form,
               'payment_form': payment_form,
               'publishable': settings.STRIPE_PUBLISHABLE}
    context = is_premium(request.user, context)

    return render(request, 'premium/premium.html', context)


# install stripe with pip - what else?
