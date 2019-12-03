from django.shortcuts import render, get_object_or_404

import copy
import json

from premium.utils import is_premium
from .models import Bookmark, Collection, Page
# from .utils import change_num_columns


# Create your views here.
def links(request):
    page_name = "home"  # temp for now, until built into path

    bookmarks = Bookmark.objects.filter(
        user__username=request.user
        )
    collections = Collection.objects.filter(
        user__username=request.user).filter(
        page__name=page_name
        )
    page = get_object_or_404(
        Page, user=request.user, name=page_name
    )

    num_of_columns = page.num_of_columns

    if num_of_columns != 1:
        # get the display order for the collections from the db
        collection_order = json.loads(
            eval('page.collection_order_'+str(page.num_of_columns)))
        collection_list = copy.deepcopy(collection_order)
        # put collection names into a list. add them in order based on
        # the value of collection.position and map this to the structure
        # of collection_list
        count = 0
        for col in range(num_of_columns):
            for pos in range(len(collection_order[col])):
                count += 1
                collection_name = get_object_or_404(
                    Collection,
                    user=request.user,
                    position=count
                )
                collection_list[col][pos] = str(collection_name)
    else:
        # single columm collection display
        collection_list = [[]]
        for i in range(collections.count()):
            collection_name = get_object_or_404(
                Collection,
                user=request.user,
                position=i+1
            )
            collection_list[0].append(str(collection_name))

    # iterate through collection names and create a qs of bookmarks for each
    bm_data = []
    for x in range(num_of_columns):
        column = {}
        for j in (collection_list[x]):
            qs = bookmarks.filter(collection__name=j).order_by('position')
            column[j] = qs
        bm_data.append(column)

    context = {"column_width": 100 / num_of_columns,
               "bm_data": bm_data,
               "page": page_name}
    context = is_premium(request.user, context)

    return render(request, 'links/links.html', context)
