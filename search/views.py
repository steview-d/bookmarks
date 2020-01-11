from django.shortcuts import render

from premium.utils import is_premium

from links.models import Page, Bookmark


# Create your views here.
def search(request):
    # Fetch form search query
    q = request.GET.get('q')

    # find bookmarks based on search query
    search_results = Bookmark.objects.filter(
        user=request.user, title__icontains=q
    )

    # get pages for sidebar
    all_pages = Page.objects.filter(user=request.user).order_by('position')

    # set page value for default page choice for 'add bookmark' button
    try:
        page = request.session['last_page']

    except KeyError:
        page = Page.objects.get(user=request.user, position=1)

    context = {
        "all_page_names": all_pages,
        "page": page,
        "q": q,
        "search_results": search_results
    }
    context = is_premium(request.user, context)

    return render(request, 'search/search_results.html', context)
