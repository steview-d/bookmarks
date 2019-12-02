from django.shortcuts import render, get_object_or_404

import copy

from premium.utils import is_premium
from .models import Bookmark, Collection


# Create your views here.
def links(request):

    bookmarks = Bookmark.objects.filter(user__username=request.user)
    collections = Collection.objects.filter(user__username=request.user)
    num_of_columns = 2  # noqa
    # eventually store this in relevant page object / model
    # just a 2d array in list form
    column_order_2 = [[1, 2, 3], [4, 5]]  # noqa
    column_order_3 = [[1, 2], [3, 4], [5]]  # noqa
    # using this one for now
    column_order_4 = [[1], [2], [3], [4, 5]]  # noqa

    # add if statement for single column display
    if num_of_columns != 1:
        # create list structure to store column names
        # arg below eventually to be dynamically chosen based on user pref
        new_column_output = copy.deepcopy(column_order_2)
        # put collection names into array in column order...
        count = 0
        for col in range(num_of_columns):
            for pos in range(len(column_order_2[col])):
                count += 1
                collection_name = get_object_or_404(
                    Collection,
                    user=request.user,
                    position=count
                )
                new_column_output[col][pos] = str(collection_name)
    else:
        # single columm collection display
        new_column_output = [[]]
        for i in range(collections.count()):
            collection_name = get_object_or_404(
                Collection,
                user=request.user,
                position=i+1
            )
            new_column_output[0].append(str(collection_name))

    print(new_column_output)

    # iterate through collection names and create a qs of bookmarks for each
    bm_data = []
    for x in range(num_of_columns):
        column = {}
        for j in (new_column_output[x]):
            qs = bookmarks.filter(collection__name=j).order_by('position')
            column[j] = qs
        bm_data.append(column)

    context = {"num_columns": num_of_columns,
               "bm_data": bm_data}
    context = is_premium(request.user, context)

    return render(request, 'links/links.html', context)
