from django.shortcuts import render

from premium.utils import is_premium
from .models import Bookmark, Collection


# Create your views here.
def links(request):

    # put names of all the current users collections into a list
    # collections = Collection.objects.filter(user__username=request.user)
    # collection_list = []
    # for collection in collections:
    #     collection_list.append(collection.name)

    bookmarks = Bookmark.objects.filter(user__username=request.user)
    collections = Collection.objects.filter(user__username=request.user)

    # build a dictionary of collection names, with column numbers as the key
    collection_dict = {}
    for column_num in range(1, 5):
        for collection in collections:
            if collection.column == column_num:
                try:
                    collection_dict[column_num] += [collection.name]
                except KeyError:
                    collection_dict[column_num] = [collection.name]

    # column_list = ['column-1', 'column-2', 'column-3', 'column-4']

    # for i in range(len(column_list)):
    #     pass

    column_1 = {}
    column_2 = {}
    column_3 = {}
    column_4 = {}


    for i in (collection_dict[1]):
        qs = bookmarks.filter(collection__name=i).order_by('position')
        column_1[i] = qs

    for i in (collection_dict[2]):
        qs = bookmarks.filter(collection__name=i).order_by('position')
        column_2[i] = qs

    # create a dictionary to hold collections of bookmarks
    # collection_stuff = {}

    # for i in range(len(collection_list)):
    #     qs = bookmarks.filter(
    #         collection__name=collection_list[i]).order_by('position')
    #     collection_dict[collection_list[i]] = qs

    # for column in range(1, 5):

    context = {'collections': column_1, 'coll_2': column_2}
    context = is_premium(request.user, context)

    return render(request, 'links/links.html', context)
