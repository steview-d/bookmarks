from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from links.utils import bookmark_utils
from premium.utils import is_premium

from links.models import Page, Bookmark
from links.utils.general_utils import set_page_name


# Create your views here.

@login_required
def search(request):

    # delete bookmark
    if 'delete-bookmark-form' in request.POST:
        bookmark_utils.delete_bookmark(request)

    # Fetch form search query
    q = request.GET.get('q')
    q = "" if q is None else q

    # find bookmarks based on search query
    search_qs = Bookmark.objects.filter(
        user=request.user, title__icontains=q
    ).order_by('added')

    # pagination
    results_page = request.GET.get('rpage', 1)

    paginator = Paginator(search_qs, 5)
    try:
        search_results = paginator.page(results_page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    # get pages for sidebar
    all_pages = Page.objects.filter(user=request.user).order_by('position')

    # set page value for default page choice for 'add bookmark' button
    page = set_page_name(request)

    context = {
        "all_page_names": all_pages,
        "page": page,
        "q": q,
        "search_results": search_results,
        "p": paginator,
        "page_num": results_page,
    }
    context = is_premium(request.user, context)

    return render(request, 'search/search_results.html', context)
