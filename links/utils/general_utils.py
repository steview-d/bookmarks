from django.shortcuts import redirect

from links.models import Page

from .page_utils import create_default_page


def start_app(request):
    """
    This function runs when coming to the main app from the bm icon logo
    or after logging in.
    It first checks the user has at least 1 page. If no pages are found,
    the app will create a default 'home' page for the user.
    If pages already exists,  the app will either point to last page
    visited, which is stored in session, or if no session value, it will
    load the page at position 1.

    Args:
        request (obj): The request object
    """

    # check if user has at least 1 page and if not, create one & redirect to it
    if not Page.objects.filter(user=request.user).exists():
        create_default_page(request)

    # get last page data and redirect if applicable, otherwise load first page
    try:
        last_page = request.session['last_page']

    except KeyError:
        last_page = Page.objects.get(user=request.user, position=1)
        request.session['last_page'] = last_page.name

    return redirect('links', page=last_page)
