from django.shortcuts import redirect, render, reverse


# Create your views here.
def about(request):
    # redirect if a user is already logged in
    if request.user.is_authenticated:
        # eventually will be main app page
        return redirect(reverse('profile'))

    return render(request, "pages/index.html")


def pricing(request):
    # redirect if a user is already logged in
    if request.user.is_authenticated:
        # eventually will be main app page
        return redirect(reverse('profile'))

    return render(request, "pages/pricing.html")


def faq(request):
    # redirect if a user is already logged in
    if request.user.is_authenticated:
        # eventually will be main app page
        return redirect(reverse('profile'))

    return render(request, "pages/faq.html")
