from django.shortcuts import redirect, render, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

# from django.contrib import auth


# Create your views here.
@login_required
def logout(request):
    """ Log out the current user """
    auth.logout(request)
    # messages.success(request, "Log out successful")
    return redirect(reverse('about_page'))


def register(request):
    return render(request, 'accounts/register.html')
