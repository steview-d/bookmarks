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

    # bump positions +1 for any position after 'insert_at_position'
    all_collections = Collection.objects.filter(
        user=request.user, page=page).order_by('-position')

    # comment out while work on updating collection_order_x lists
    # below updates the all_collections qs, and *seems* to work fine
    #
    # for collection in all_collections:
    #     if collection.position >= insert_at_position:
    #         collection.position += 1
    #         collection.position.save()

    # check if adding to an empty column
    is_empty = request.POST.get('is_empty')
    print("IS EMPTY: ", is_empty)

    # update collection_order_x list values
    for i in range(2, 6):
        print("NUM COLUMNS: ", i)
        collection_order = json.loads(
            eval('page.collection_order_'+str(i)))
        print("----------------------------")
        print("BEFORE: ", collection_order)
        # print("----------------------------")
        # print("COLUMN CLICKED ", column)

        for col in range(len(collection_order)):
            for pos in range(len(collection_order[col])):
                # insert new collection in correct place

                # +1 to all collections at or after insert position
                if collection_order[col][pos] >= insert_at_position:
                    collection_order[col][pos] += 1

                if collection_order[col][pos] == insert_at_position - 1:
                    # print("PUT HERE: ", collection_order[col][pos])
                    # print("COL: ", col, "  |  ", "POS: ", pos)
                    if not is_empty:
                        collection_order[col].append(insert_at_position)

        if is_empty and i == page.num_of_columns:
            collection_order[int(column)-1] = [insert_at_position]

        if is_empty and i != page.num_of_columns:
            for col in range(len(collection_order)):
                if insert_at_position - 1 in collection_order[col]:
                    collection_order[col].append(insert_at_position)

        # inserting into columns of different layouts to the one the user
        # is inserting into can cause new collections to be added to the end,
        # and not in the correct place. This fixes that.
        for col in range(len(collection_order)):
            collection_order[col].sort()

        print("----------------------------")
        print("AFTER:  ", collection_order)
        print("----------------------------")

    # not convinced right way......
    # if page.num_of_columns > 1:
    #     print()
    #     collection_order_after_insert = collection_order[int(column):]
    #     print("BEFORE: ", collection_order_after_insert)

    #     for col in range(len(collection_order_after_insert)):
    #         for pos in range(len(collection_order_after_insert[col])):
    #             collection_order_after_insert[col][pos] += 1
    #     print("AFTER: ", collection_order_after_insert)

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
