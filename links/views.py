from django.shortcuts import render

from premium.utils import is_premium
from .models import Bookmark, Collection


# Create your views here.
def links(request):

    bookmarks = Bookmark.objects.filter(user__username=request.user)
    collections = Collection.objects.filter(user__username=request.user)
    num_of_columns = 4
    print(num_of_columns)

    # build a dictionary of collection names, with column numbers as the key
    collection_dict = {}
    for column_num in range(1, 5):
        for collection in collections:
            if collection.column == column_num:
                try:
                    collection_dict[column_num] += [collection.name]
                except KeyError:
                    collection_dict[column_num] = [collection.name]
    for k, v in collection_dict.items():
        print(k, v)

    # alt version - build a dict of collection names
    # 1 key per column, and num keys / columns to be
    # based on value of 'num_of_columns'

    # instead of column and position, maybe just position?
    # if position stays constant, and so do columns, would overall order?
    # how would define breakpoint? how keep it consistent?
    # on column no' swap - auto define breakpoints?

    #

    # column_list = ['column_1', 'column_2', 'column_3', 'column_4']
    column_1 = {}
    column_2 = {}
    column_3 = {}
    column_4 = {}

    # this to be tidied...
    for i in (collection_dict[1]):
        qs = bookmarks.filter(collection__name=i).order_by('position')
        column_1[i] = qs

    for i in (collection_dict[2]):
        qs = bookmarks.filter(collection__name=i).order_by('position')
        column_2[i] = qs

    for i in (collection_dict[3]):
        qs = bookmarks.filter(collection__name=i).order_by('position')
        column_3[i] = qs

    for i in (collection_dict[4]):
        qs = bookmarks.filter(collection__name=i).order_by('position')
        column_4[i] = qs

    all_collections = [column_1, column_2, column_3, column_4]

    context = {'all_collections': all_collections}
    context = is_premium(request.user, context)

    return render(request, 'links/links.html', context)
