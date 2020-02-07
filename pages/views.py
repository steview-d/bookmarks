from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import ContactForm


# Create your views here.
def about(request):
    # redirect if a user is already logged in
    if request.user.is_authenticated:
        return redirect('start_app')

    context = {}

    return render(request, "pages/index.html", context)


def pricing(request):
    # redirect if a user is already logged in
    if request.user.is_authenticated:
        return redirect('start_app')

    # data for pricing comparison table
    table_data = [
        ['Feature', 'Free', 'Premium'],
        ['Ads', 'Ad Supported', 'No Ads. Ever'],
        ['Bookmarks', '500', 'Unlimited'],
        ['Collections', '20', 'Unlimited'],
        ['Pages', '2', 'Unlimited'],
        ['Support', 'Email', 'Email & Telephone'],
        ['Cost', 'Free', '£20 for lifetime access'],
    ]

    context = {"table_data": table_data, }

    return render(request, "pages/pricing.html", context)


def faq(request):
    # redirect if a user is already logged in
    if request.user.is_authenticated:
        return redirect('start_app')

    # initialize contact form
    contact_form = ContactForm()

    # check for contact form
    if 'contact-form' in request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(
                request, f"Form sent successfully. Thank you.")

            return redirect('faq_page')

    context = {"contact_form": contact_form, }

    return render(request, "pages/faq.html", context)
