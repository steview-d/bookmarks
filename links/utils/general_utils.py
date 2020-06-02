from links.models import Page

from .page_utils import create_default_page
from .collection_utils import create_default_collection


def qs_sort(original_order, new_order, limit):
    """
    A function that updates a querysets .position field values.

    Args:
        original_order (qs): A qs of objects ordered by .position field
        new_order (list): A list containing the new order for the qs
        limit (int): The (current) max allowed number of objects per
                     user of type matching 'original_order' queryset.

    Returns:
        dict : A dict to pass pack to the front end with JsonResponse

    """

    for idx, item in enumerate((original_order), 1):
        item.position_temp = new_order.index(item.position) + 1
        item.position = idx + limit
        item.save()

    for item in original_order:
        item.position = item.position_temp
        item.position_temp = None
        item.save()

    return {'success': True}


def set_page_name(request):
    """
    small helper function to set the page name so it can be passed as
    an argument when required.
    For example, the 'add bookmark' button requires a value for page so
    it can choose a default destination page / collection combination
    for the user on page load
    """

    try:
        page = request.session['last_page']

    except KeyError:
        page = Page.objects.get(user=request.user, position=1)

    return page


def new_user_setup(request):
    """
    When a new user is created, app should create a new page, a new
    collection, and 5 new bookmarks, to provide the user with initial
    content so they can see how it all works.
    """

    create_default_page(request)
    create_default_collection(request)

    return
