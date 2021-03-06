from django.contrib import messages


def is_premium(request, context):
    """
    Checks if the passed user is a member of the 'Premium' group
    if so, {'is_premium': True} is added to the 'context' dict

    Args:
        request (obj) : request.user
        context (dict): the context dict that will be passed to the
                        template

    Returns:
        The 'context' dict

    """

    if request.groups.filter(name__in=['Premium']).exists():
        context['is_premium'] = True
    return context


def premium_check(request, model, settings_value):
    """
    Check if user status allows them to add another item

    Args:
        request : request.user
        model : The model being checked against
                - Bookmark, Collection or Page
        settings_value : The settings value to check against

    Returns:
        Bool
    """

    num_items = model.objects.filter(
        user=request.user
    ).count()

    premium_check = request.user.groups.filter(name__in=['Premium']).exists()

    if not premium_check and num_items >= settings_value:
        messages.error(
            request, f"Standard members may have at most \
                {settings_value} {model.__name__}s. \
                To add more, become a Premium member.")
        return False

    return True
