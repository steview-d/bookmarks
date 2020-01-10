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
