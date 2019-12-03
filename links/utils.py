from django.shortcuts import get_object_or_404, redirect, reverse

from .models import Page


def change_num_columns(request, page, num):
    if int(num) > 0 and int(num) < 6:
        page = get_object_or_404(
            Page, user=request.user, name=page
        )
        page.num_of_columns = num
        page.save()
    return redirect(reverse('links'))
