from django.shortcuts import render

from premium.utils import is_premium


# Create your views here.
def links(request):

    context = {}
    context = is_premium(request.user, context)

    return render(request, 'links/links.html', context)
