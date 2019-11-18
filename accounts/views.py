from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordChangeForm
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

    # if "email-btn" in request.POST:
    #     return

    # elif "pw-btn" in request.POST:
    #     return

    if request.method == "POST":
        print(request)
        update_email_form = UpdateUserEmailForm(
            request.POST, instance=request.user)
        password_change_form = PasswordChangeForm(
            request.POST)

        if update_email_form.is_valid() or password_change_form.is_valid():
            update_email_form.save()
            password_change_form.save()
            return redirect(reverse("profile"))

    else:
        update_email_form = UpdateUserEmailForm()
        password_change_form = PasswordChangeForm(request.user)

    context = {"profile": user,
               "update_email_form": update_email_form,
               "password_change_form": password_change_form}

    return render(request, 'accounts/profile.html', context)


@login_required
def support(request):

    context = {}

    return render(request, 'accounts/support.html', context)


@login_required
def about(request):

    context = {}

    return render(request, 'accounts/about.html', context)
