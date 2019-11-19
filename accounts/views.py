from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
# from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse
# from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegisterAccountForm, UpdateUserEmailForm
from support.forms import SupportRequestForm


from django.contrib.auth import update_session_auth_hash


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

    if "email-btn" in request.POST:
        password_change_form = PasswordChangeForm(request.user)
        update_email_form = UpdateUserEmailForm(
            request.POST, instance=request.user)

        if update_email_form.is_valid():
            update_email_form.save()
            return redirect(reverse("profile"))

    elif "pw-btn" in request.POST:
        update_email_form = UpdateUserEmailForm()
        password_change_form = PasswordChangeForm(
            user=request.user, data=request.POST)

        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
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

    if request.method == "POST":
        form_data = SupportRequestForm(request.POST)
        if form_data.is_valid():
            form = form_data.save(commit=False)
            form.username = request.user
            form.email = request.user.email
            form.save()

            # username = form_data.cleaned_data.get('username')
            # email = form_data.cleaned_data.get('email')
            # title = form_data.cleaned_data.get('title')
            # message = form_data.cleaned_data.get('message')
            # print(email)
            # send_mail(title, message, 'Bookmark Team', [email])

        return redirect(reverse("support"))

    else:
        support_request_form = SupportRequestForm()

    context = {"support_request_form": support_request_form}

    return render(request, 'accounts/support.html', context)


@login_required
def about(request):

    context = {}

    return render(request, 'accounts/about.html', context)
