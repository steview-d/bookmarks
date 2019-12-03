from django.shortcuts import get_object_or_404, redirect

from .models import Page


def start_app(request):
    # function to load app when coming from bm icon log or after first
    # logging in will either point to page stored in session, or if no
    # session default to page position value of 1
    return redirect('links', page='home')


def change_num_columns(request, page, num):
    if int(num) > 0 and int(num) < 6:
        page = get_object_or_404(
            Page, user=request.user, name=page
        )
        page.num_of_columns = num
        page.save()
    return redirect('links', page='home')
