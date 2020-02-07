from django.shortcuts import redirect, render


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

    context = {"table_data": table_data}

    return render(request, "pages/pricing.html", context)


def faq(request):
    # redirect if a user is already logged in
    if request.user.is_authenticated:
        return redirect('start_app')

    context = {}

    return render(request, "pages/faq.html", context)
