from django.shortcuts import get_object_or_404, redirect

from .models import Page


def start_app(request):
    """
    This function loads the app when coming from bm icon logo or after
    logging in. It will either point to page the last page visited,
    stored in session, or if no session value, it will load the page at
    position 1.
    """
    try:
        last_page = request.session['last_page']

    except KeyError:
        last_page = Page.objects.get(user=request.user, position=1)
        request.session['last_page'] = last_page.name

    return redirect('links', page=last_page)


def change_num_columns(request, page, num):
    if int(num) > 0 and int(num) < 6:
        page = get_object_or_404(
            Page, user=request.user, name=page
        )
        page.num_of_columns = num
        page.save()
    return redirect('links', page=page.name)


def add_new_page(request):
    """
    Use this to build a new page.
    Needs to not only create a new page object, but also
    configure it so it has al required default info so it
    can display ok, for instance
    - Name, position, column order lists, etc
    """
