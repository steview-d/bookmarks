from django.shortcuts import render

from premium.utils import is_premium

from links.models import Page


# Create your views here.
def search(request):

    # set page value for default page choice for 'add bookmark' button
    try:
        page = request.session['last_page']

    except KeyError:
        page = Page.objects.get(user=request.user, position=1)

    all_pages = Page.objects.filter(user=request.user).order_by('position')

    context = {
        "all_page_names": all_pages,
        "page": page,
    }
    context = is_premium(request.user, context)

    return render(request, 'search/search_results.html', context)
