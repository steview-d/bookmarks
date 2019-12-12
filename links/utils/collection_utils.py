from django.contrib import messages
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect

import itertools
import json
import re

from links.models import Page, Collection


def change_num_columns(request, page, num):
    """
    Changes the number of columns the current page will use
    to display content

    Args:
        request (obj): The request object
        page (obj) : The current page
        num (str) : The number of columns the user has requested

    """
    if int(num) > 0 and int(num) < 6:
        page = get_object_or_404(
            Page, user=request.user, name=page
        )
        page.num_of_columns = num
        page.save()
    return redirect('links', page=page.name)


def validate_name(request, collections, page):
    """
    Check the requested name contains no unallowed chars and that the
    name is unique to the current page and user.
    """
    proposed_name = request.POST.get('collection_name')

    # check name contains only allowed chars
    allowed_chars = re.compile(r'[^-: a-zA-Z0-9.]')
    char_check = allowed_chars.search(proposed_name)
    if char_check:
        messages.error(
            request, f"Name can only contain letters, numbers, \
                        spaces, hyphens '-', and colons ':'")
        # return redirect('links', page=page)
        return False

    # check collection name is unique to page / user
    elif collections.filter(
            name=request.POST.get('collection_name')).exists():
        messages.error(
            request, f"Collection name is in use, please choose another")
        # return redirect('links', page=page)
        return False
    else:
        return True


def add_collection(request, current_page):
    """
    This function adds a new collection to the current page.
    It updates the .position value of each collection within the page
    and also the .collection_order_[x] values that decide how the collections
    are displayed on each page, for each number of columns.

    Outside of any column ordering, the collections are ordered using the
    .position var and this runs from 1 through to the total number of
    collections the pages contains.

    Whenever a new collection is added, the 'insert_at_position' var is created
    to show where in the order the new collection should be added.

    Any collections with a position >= to this value have their .position value
    increased by 1 to make room for the new addition.

    Collections are displayed in a grid format. There can be between 1 and 5
    columns of collections per page, and any number of collections per column.

    This is represented with a 2d list, named .collection_order_[x], where [x]
    is the number of columns for that order. The list values are integers which
    map to the .position value for each collection.

    On adding a new collection, each collection order is updated by adding the
    new collection value to the list, in a place the func determines as best.

    The function will always try to group collections in a similar fashion
    across all column layout options. Even though it isn't expected that a user
    will regularly switch between layout options on the same screen display,
    if / when they do, the order they made will be preserved as best it can.

    Args:
        request (obj): The request object
        current_page (obj) : The current page
    """

    page = get_object_or_404(
            Page, user=request.user, name=current_page
        )
    all_collections = Collection.objects.filter(
        user=request.user, page=page).order_by('-position')

    column = int(request.POST.get('column'))
    is_empty = request.POST.get('is_empty')
    new_collection_orders = []

    # determine position within page the new collection should be inserted at
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

        # keep only positions below user specified insertion point
        collection_order_up_to_column = collection_order[:column]

        # get last (highest) value, and add 1
        flatten_order = list(itertools.chain(*collection_order_up_to_column))
        insert_at_position = flatten_order[-1] + 1 if flatten_order else 1

    all_collections = Collection.objects.filter(
        user=request.user, page=page).order_by('-position')

    # bump positions +1 for any .position after 'insert_at_position'
    for collection in all_collections:
        if collection.position >= insert_at_position:
            collection.position += 1
            collection.save()

    # update collection_order_x list values
    for i in range(2, 6):
        collection_order = json.loads(
            eval('page.collection_order_'+str(i)))

        for col in range(len(collection_order)):
            for pos in range(len(collection_order[col])):
                # +1 to all collections at or after insert position
                if collection_order[col][pos] >= insert_at_position:
                    collection_order[col][pos] += 1

                # add collection if current position has existing collections
                if (collection_order[col][pos] == insert_at_position - 1 and
                        not is_empty):
                    collection_order[col].append(insert_at_position)

        # if adding to an empty column
        if is_empty:
            if i != page.num_of_columns:
                # decide where to place new collection on other layouts.
                # if a column doesn't exist on a layout, place as close as
                # possible, working backwards from the last column
                insert_column = i if column > i else column
                collection_order[insert_column-1].append(
                    insert_at_position)
            else:
                # if inserting into current column layout, just add in place
                collection_order[column-1] = [insert_at_position]

        # inserting into columns of different layouts to the one the user
        # is inserting into can cause new collections to be added to the end,
        # and not in the correct order. This fixes that.
        for col in range(len(collection_order)):
            collection_order[col].sort()

        # store new collection orders inside a list ready to put back into db
        new_collection_orders.append(collection_order)

    # save new page collection orders to db
    page.collection_order_2 = new_collection_orders[0]
    page.collection_order_3 = new_collection_orders[1]
    page.collection_order_4 = new_collection_orders[2]
    page.collection_order_5 = new_collection_orders[3]
    page.save()

    # add new collection to db
    new_collection = Collection()
    new_collection.user = request.user
    new_collection.page = Page.objects.get(name=current_page)
    new_collection.name = request.POST.get('collection_name')
    new_collection.position = insert_at_position
    new_collection.save()

    return


def delete_collection(request):
    """
    Function to remove a collection from the db, and re-order
    position values to reflect the changes due to the deleted
    collection.
    """

    return
