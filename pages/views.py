from django.shortcuts import render


# Create your views here.
def about(request):
    return render(request, "pages/index.html")


def pricing(request):
    return render(request, "pages/pricing.html")


def faq(request):
    return render(request, "pages/faq.html")
