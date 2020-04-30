from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import SupportRequestForm
from links.utils.general_utils import set_page_name
from premium.utils import is_premium


@login_required
def support(request):
    # if support form has been posted
    if request.method == "POST":
        form_data = SupportRequestForm(request.POST)
        if form_data.is_valid():
            # save support form to db
            form = form_data.save(commit=False)
            form.user = request.user
            form.email = request.user.email
            form.save()

            html_message = render_to_string(
                'support/support_email_template.html',
                {'title': form.title,
                 'message': form.message,
                 'username': form.user})
            plain_message = strip_tags(html_message)

            # email user a copy of their support form
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
            messages.error(
                request, f"There was an error with your form, \
                    please try again."
            )
            support_request_form = form_data

    else:
        support_request_form = SupportRequestForm()

    # set page value for default page choice for 'add bookmark' button
    page = set_page_name(request)

    context = {'support_request_form': support_request_form,
               'page': page,
               }
    context = is_premium(request.user, context)

    return render(request, 'support/support.html', context)
