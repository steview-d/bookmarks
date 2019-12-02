from django.shortcuts import render, get_object_or_404

import copy

from premium.utils import is_premium
from .models import Bookmark, Collection


# Create your views here.
def links(request):

    bookmarks = Bookmark.objects.filter(user__username=request.user)
    num_of_columns = 4  # noqa
    # eventually store this in relevant page object / model
    # just a 2d array in list form
    column_order_2 = [[1, 2, 3], [4, 5]]  # noqa
    column_order_3 = [[1, 2], [3, 4], [5]]  # noqa
    # using this one for now
    column_order_4 = [[1], [2], [3], [4, 5]]  # noqa

    # arg below eventually needs to be dynamically chosen based on user pref
    new_column_output = copy.deepcopy(column_order_4)

    # put collection names into array in column order...
    for col in range(num_of_columns):
        for pos in range(len(column_order_4[col])):
            collection_name = get_object_or_404(
                Collection,
                user=request.user,
                column=col+1,
                position=pos+1
            )
            new_column_output[col][pos] = str(collection_name)

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
