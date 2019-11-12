from django.shortcuts import redirect, render, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

# from django.contrib import auth


# Create your views here.
def register(request):
    return render(request, 'accounts/register.html')
