from django.shortcuts import redirect

from links.models import Page


def start_app(request):
    """
    This function loads the app when coming from bm icon logo or after
    logging in. It will either point to page the last page visited,
    stored in session, or if no session value, it will load the page at
    position 1.

    Args:
        request (obj): The request object
    """

    # ## TO DO ###
    # needs to check if any pages exist for current user, eg if a users
    # first visit.
    # if so, need to create a new page and set up collection orders etc.
    # Can give a default name like 'home'

    try:
        last_page = request.session['last_page']

    except KeyError:
        last_page = Page.objects.get(user=request.user, position=1)
        request.session['last_page'] = last_page.name

    return redirect('links', page=last_page)
