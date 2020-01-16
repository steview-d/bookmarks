from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

import requests as req
from links.models import Collection, Bookmark


def delete_bookmark(request):
    """
    Find and delete the requested bookmark using its pk from
    request.POST and then reset the 'position' values for all remaining
    bookmarks within the collection to run in order again.
    """

    # get bookmark that is to be deleted
    bookmark_to_delete = get_object_or_404(
        Bookmark, pk=request.POST.get('bookmark')
    )

    # get collection that bookmark is a part of
    bookmark_collection = get_object_or_404(
        Collection, pk=bookmark_to_delete.collection.id
    )

    bookmark_to_delete.delete()

    # get remaining bookmarks, in position order
    all_bookmarks_in_collection = Bookmark.objects.filter(
        collection=bookmark_collection
    ).order_by('position')

    reorder_bookmarks(all_bookmarks_in_collection)

    return


def reorder_bookmarks(bookmark_qs):
    """
    Iterate through a queryset of bookmarks and apply the .position
    value, in order.
    """

    for count, bm in enumerate((bookmark_qs), 1):
        bm.position = count
        bm.save()

    return


def scrape_url(request, url):
    """
    Scrape metadata from a URL using BeautifulSoup4
    """

    # some sites refuse to play nicely unless we're sneaky and throw some
    # browser headers over too
    headers = {'User-Agent': 'Mozilla/5.0'}

    # default return data
    data = {'message': 'The URL is empty',
            'title': '',
            'description': ''}

    if not url:
        return JsonResponse(data)

    try:
        r = req.get(url, headers=headers)
        r.raise_for_status()

    except req.exceptions.RequestException:
        data['message'] = 'Could not load this URL'

    else:
        soup = BeautifulSoup(r.text, 'html.parser')

        # get the page title
        scraped_title = soup.title.get_text() if soup.title.get_text() else \
            "Could not retrieve a title"

        # get the page description from metadata content
        metas = soup.find_all('meta')
        for m in metas:
            if 'name' in m.attrs and m.attrs['name'] == 'description':
                scraped_description = m.attrs['content']

        # provide default response for when no metadata available
        try:
            scraped_description
        except UnboundLocalError:
            scraped_description = "Sorry, no metadata available for this URL"

        # handle empty description metadata
        if scraped_description == '':
            scraped_description = "Sorry, no metadata available for this URL"

        data = {'message': 'Success',
                'title': scraped_title,
                'description': scraped_description}

    return data
