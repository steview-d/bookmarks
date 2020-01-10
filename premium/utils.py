from links.conf import settings
from django.contrib import messages

from links.models import Page


def is_premium(request, context):
    """
    checks if the passed user is a member of the 'Premium' group
    if so, {'is_premium': True} is added to the 'context' dict

    Args:
        request : request.user
        context : the context dict that will be passed to the template

    Returns:
        The 'context' dict

    """

    if request.groups.filter(name__in=['Premium']).exists():
        context['is_premium'] = True
    return context


def premium_check(request):
    """
    checks if the passed user is a member of the 'Premium' group and
    returns either True or False
    """

    return request.user.groups.filter(name__in=['Premium']).exists()


def premium_check_add_page(request, page):
    """
    Check if user status allows them to add another page

    Returns:
        Bool
    """

    num_pages = Page.objects.filter(
        user=request.user
    ).count()

    if not premium_check(request) and \
            num_pages >= settings.LINKS_STND_MAX_PAGES:
        messages.error(
            request, f"Standard members may have at most 2 pages. \
                To add more, become a Premium member.")
        return False

    return True
