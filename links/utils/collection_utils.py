from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect

import itertools
import json

from links.models import Page, Collection


def change_num_columns(request, page, num):
    if int(num) > 0 and int(num) < 6:
        page = get_object_or_404(
            Page, user=request.user, name=page
        )
        page.num_of_columns = num
        page.save()
    return redirect('links', page=page.name)


def add_collection(request, current_page):
    # this should be fun...

    # iterate in reverse, each num do num+1 until
    # you reach new pos num, then append a new entry
    # to end of specified column
    # do for each set of colums, 2 through 5

    page = get_object_or_404(
            Page, user=request.user, name=current_page
        )
    all_collections = Collection.objects.filter(
        user=request.user, page=page).order_by('-position')

    # determine what position within page the
    # new collection should be inserted at
    if page.num_of_columns == 1:
        # get highest 'position' value and +1
        if all_collections.count() > 0:
            max_pos_value = all_collections.aggregate(
                    Max('position')
            )
            insert_at_position = (max_pos_value['position__max'] + 1)
        else:
            insert_at_position = 1
    else:
        # get collection positions for current layout
        collection_order = json.loads(
            eval('page.collection_order_'+str(page.num_of_columns)))
        # keep only positions below user specified entry point
        column = request.POST.get('column')
        collection_order_up_to_column = collection_order[:int(column)]
        # get highest value. num of values, last value, and add 1
        flatten_order = list(itertools.chain(*collection_order_up_to_column))
        insert_at_position = flatten_order[-1] + 1 if flatten_order else 1

    print("INSERT AT: ", insert_at_position)
    all_collections = Collection.objects.filter(
        user=request.user, page=page).order_by('-position')

    # update all position nums for each collection

    # update collection_order_x list values

    # insert new collection into collection order_x lists

    # comment out below temp only whilst testing....
    # new_collection = Collection()
    # new_collection.user = request.user
    # new_collection.page = Page.objects.get(name=current_page)
    # new_collection.name = "qwerty"
    # new_collection.position = 100  # need to shufle rest along first
    # new_collection.save()

    # print("PAGE: ", page)
    # print("COLUMN: ", request.POST.get('column'))
    # print("POSITION: ", request.POST.get('position'))

    return
