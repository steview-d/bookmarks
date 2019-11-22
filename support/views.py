from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import SupportRequestForm
from premium.utils import is_premium


# Create your views here.
@login_required
def support(request):

    if request.method == "POST":
        form_data = SupportRequestForm(request.POST)
        if form_data.is_valid():
            form = form_data.save(commit=False)
            form.username = request.user
            form.email = request.user.email
            form.save()

            html_message = render_to_string(
                'support/support_email_template.html',
                {'title': form.title,
                 'message': form.message,
                 'username': form.username})
            plain_message = strip_tags(html_message)

            send_mail(form.title,
                      plain_message,
                      'Bookmark Team',
                      [form.email],
                      html_message=html_message
                      )

            messages.success(
                request, "Ticket created, we'll be in touch soon!")

        return redirect(reverse("support"))

    else:
        support_request_form = SupportRequestForm()

    context = {"support_request_form": support_request_form}
    context = is_premium(request.user, context)

    return render(request, 'support/support.html', context)
