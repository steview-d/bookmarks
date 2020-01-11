from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, reverse

from .forms import RegisterAccountForm, UpdateUserEmailForm
from links.utils.general_utils import set_page_name
from premium.utils import is_premium


# views
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
def profile(request):
    """ The current users profile page """
    user = User.objects.get(email=request.user.email)

    if "email-btn" in request.POST:
        password_change_form = PasswordChangeForm(request.user)
        update_email_form = UpdateUserEmailForm(
            request.POST, instance=request.user)

        if update_email_form.is_valid():
            update_email_form.save()
            messages.success(
                request, f"Your email address has been updated. Thank you.")
            return redirect(reverse("profile"))

    elif "pw-btn" in request.POST:
        update_email_form = UpdateUserEmailForm()
        password_change_form = PasswordChangeForm(
            user=request.user, data=request.POST)

        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
            messages.success(
                request, f"Your password has been updated. Thank you.")
            return redirect(reverse("profile"))

    else:
        update_email_form = UpdateUserEmailForm()
        password_change_form = PasswordChangeForm(request.user)

    # set page value for default page choice for 'add bookmark' button
    page = set_page_name(request)

    context = {"profile": user,
               "update_email_form": update_email_form,
               "password_change_form": password_change_form,
               "page": page}
    context = is_premium(request.user, context)

    return render(request, 'accounts/profile.html', context)


@login_required
def about(request):
    # set page value for default page choice for 'add bookmark' button
    page = set_page_name(request)

    context = {'app_version': settings.LINKS_APP_VERSION,
               'page': page,
               }
    context = is_premium(request.user, context)

    return render(request, 'accounts/about_app.html', context)
