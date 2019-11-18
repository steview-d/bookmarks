from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, reverse
# from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegisterAccountForm, UpdateUserEmailForm


# from django.contrib import auth


# Create your views here.
def register(request):
    # redirect if a user is already logged in
    if request.user.is_authenticated:
        # eventually will be main app page
        return redirect(reverse('profile'))

    # handle posted form data
    if request.method == "POST":
        form = RegisterAccountForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('about_page')
    else:
        form = RegisterAccountForm()

    context = {'form': form}

    return render(request, 'accounts/register.html', context)


@login_required
def premium(request):

    context = {}

    return render(request, 'accounts/premium.html', context)


@login_required
def profile(request):
    """ The current users profile page """
    user = User.objects.get(email=request.user.email)

    new_email = UpdateUserEmailForm(request.POST, instance=request.user)
    if new_email.is_valid():
        new_email.save()
        return redirect(reverse("profile"))

    update_email_form = UpdateUserEmailForm()

    context = {"profile": user, "update_email_form": update_email_form}

    return render(request, 'accounts/profile.html', context)


@login_required
def support(request):

    context = {}

    return render(request, 'accounts/support.html', context)


@login_required
def about(request):

    context = {}

    return render(request, 'accounts/about.html', context)
