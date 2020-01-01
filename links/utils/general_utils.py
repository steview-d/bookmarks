from django.shortcuts import redirect

from links.models import Page

from .page_utils import build_empty_collection_order


def start_app(request):
    """
    This function loads the app when coming from bm icon logo or after
    logging in.
    It first checks the user has at least 1 page. If no pages are found,
    the app will create a default 'home' page for the user.
    If pages already exists,  the app will either point to last page
    visited, which is stored in session, or if no session value, it will
    load the page at position 1.

    Args:
        request (obj): The request object
    """

    # check if any user data exists, and if not, create a page
    if not Page.objects.filter(user=request.user).exists():
        page = Page(user=request.user,
                    name="home",
                    position=1,
                    collection_order_2=build_empty_collection_order(2),
                    collection_order_3=build_empty_collection_order(3),
                    collection_order_4=build_empty_collection_order(4),
                    collection_order_5=build_empty_collection_order(5),
                    )

        page.save()
        return redirect('links', page="home")

    # get last page data and redirect if applicable, otherwise load first page
    try:
        last_page = request.session['last_page']

    except KeyError:
        last_page = Page.objects.get(user=request.user, position=1)
        request.session['last_page'] = last_page.name

    return redirect('links', page=last_page)
