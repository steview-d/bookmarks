from links.models import Page


def qs_sort(original_order, new_order, limit):
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
    an argument when required. For example the 'add bookmark' button
    requires a value for page so it can choose a default destination
    page / collection combination for the user on page load
    """
    try:
        page = request.session['last_page']

    except KeyError:
        page = Page.objects.get(user=request.user, position=1)

    return page
