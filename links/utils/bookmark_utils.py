from django.shortcuts import get_object_or_404

from links.models import Collection, Bookmark


def delete_bookmark(request):
    """
    Delete the specified bookmark and also reset the 'position' values for
    all remaining bookmarks within the collection to run in order again.
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

    all_bookmarks_in_collection = Bookmark.objects.filter(
        collection=bookmark_collection
    ).order_by('position')

    # reset position order to remove gap created by deleting bookmark
    for count, bm in enumerate((all_bookmarks_in_collection), 1):
        bm.position = count
        bm.save()

    return
