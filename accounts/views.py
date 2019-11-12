from django.shortcuts import redirect, render, reverse
from django.contrib import auth, messages

from accounts.forms import UserLoginForm
# from django.contrib import auth


# Create your views here.
def login(request):
    """ Logs a user in to the site """
    if request.user.is_authenticated:
        # later on, need to adjust the redirect to the main app view
        return redirect(reverse('about_page'))

    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])

        if user:
            auth.login(user=user, request=request)
            # messages.success(request, "Login Successful")
            return redirect(reverse('about_page'))
        else:
            login_form.add_error(
                None, "Incorret username and / or password")

    else:
        login_form = UserLoginForm()

    context = {"login_form": login_form}

    return render(request, 'accounts/login.html', context)


def register(request):
    return render(request, 'accounts/register.html')
