from django.contrib import messages
from django.db.models import Max
from django.shortcuts import get_object_or_404

import copy
import itertools
import json
import re

from links.models import Page, Collection


def validate_name(request, proposed_name, collections, page):
    """
    Check the requested name contains no disallowed chars and that the
    name is unique to the current page and user.

    Args:
        request (obj): The request object
        proposed_name (str): The name input by the user
        collections (queryset): Collections for current page and user
        page (obj): The current page

    Returns:
        Bool: True for a valid name, False if not.
    """

    # check name contains only allowed chars
    allowed_chars = re.compile(r'[^-: a-zA-Z0-9.]')
    char_check = allowed_chars.search(proposed_name)
    if char_check:
        messages.error(
            request, f"Name can only contain letters, numbers, \
                        spaces, hyphens '-', and colons ':'")
        return False

    # check collection name not blank or just spaces
    if proposed_name == '':
        messages.error(
            request, f"You must choose a name.")
        return False

    if proposed_name.isspace():
        messages.error(
            request, f"The name cannot be just blank spaces.")
        return False

    # check collection name is unique to page / user
    if collections.filter(
            name__iexact=proposed_name.strip()).exists():
        messages.error(
            request, f"Collection name is in use, please choose another.")
        return False

    else:
        return True


def make_collection_list(request, page, num_of_columns, collections):
    """
    A function which generates a 2d list of collection names,
    structured to match the current column layout, which is later used
    to create lists of bookmarks for each collection.

    Args:
        request (obj): The request object
        page (obj): The current page
        num_of_columns (int): The number of columns currently displayed
        collections (qs): A queryset of the users collections for the
                          current page

    Returns:
        list: A 2d list of all collection names for the current page.
              Every item in the list is a list of collection objects
              for a particular column. (column = list idx + 1)
    """

    if num_of_columns != 1:
        # get the collection order for the collections from the db
        collection_order = json.loads(
            eval('page.collection_order_'+str(page.num_of_columns)))
        collection_list = copy.deepcopy(collection_order)

        # starting with the collection at .position 0, map the
        # collection objects to the collection list.
        count = 0
        for col in range(num_of_columns):
            if collection_list[col] != []:
                for pos in range(len(collection_list[col])):
                    count += 1
                    collection_obj = get_object_or_404(
                        Collection,
                        page__name=page.name,
                        user=request.user,
                        position=count
                    )
                    collection_list[col][pos] = (collection_obj)
    else:
        # if there is only 1 column, add the collections to the list
        # in order of their .position value
        collection_list = [[]]
        if collections.count() > 0:
            for i in range(collections.count()):
                collection_obj = get_object_or_404(
                    Collection,
                    page__name=page.name,
                    user=request.user,
                    position=i+1
                )
                collection_list[0].append((collection_obj))

    return collection_list


def add_collection(request, page):
    """
    Create a new collection object for the current page.
    Update the .position value of each collection within the page.
    Update the .collection_order_[i] values, which store the column and
    collection structure for each page.

    Collections are ordered using .position and this runs from 1
    through to the total number of collections the page contains.

    'insert_at_position' is the position within this order that the new
    collection should be inserted.

    Any collections with a position >= to this value will have their
    .position value incremented by 1 to make room for the new addition.

    Collections are displayed in a grid format. There can be between 1
    and 5 columns per page, and any number of collections per column.

    This is represented with a 2d list, named .collection_order_[i],
    where [i] is the number of columns for that order. Each item in the
    list stores a list of integers which map to the .position value for
    each collection.

    On adding a new collection, collection orders other than the one
    currently displayed are updated by inserting the new collection
    value in the list, in a place the function determines as best.

    The function will always try to group collections in a similar
    fashion across all column layout options. Even though it isn't
    expected that a user will regularly switch between layout options
    on the same screen display, when they do, the order will be
    preserved as best it can.

    Args:
        request (obj): The request object
        current_page (obj) : The current page
    """

    all_collections = Collection.objects.filter(
        user=request.user, page=page).order_by('-position')

    column = int(request.POST.get('column'))
    is_empty = request.POST.get('is_empty')
    new_collection_orders = []

    # determine position within page the new collection should be inserted at
    if page.num_of_columns == 1:
        # get highest 'position' value and +1 for insert_at_position
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

    # update collection_order_[i] list values
    for i in range(2, 6):
        collection_order = json.loads(
            eval('page.collection_order_'+str(i)))

        for col in range(len(collection_order)):
            for pos in range(len(collection_order[col])):
                # +1 to all collections at or after insert position
                if collection_order[col][pos] >= insert_at_position:
                    collection_order[col][pos] += 1

                # add if current position has existing collections
                if (collection_order[col][pos] == insert_at_position - 1 and
                        not is_empty):
                    collection_order[col].append(insert_at_position)

        # if adding to an empty column
        if is_empty:
            if i != page.num_of_columns:
                # if a column doesn't exist on a different layout,
                # place as close as possible, working backwards from
                # the last column.
                insert_column = i if column > i else column
                collection_order[insert_column-1].append(
                    insert_at_position)
            else:
                # when inserting into the current column layout, just
                # add in place
                collection_order[column-1] = [insert_at_position]

        # inserting into columns of different layouts to the one the
        # user is inserting into can cause new collections to be added
        # to the end, and not in the correct order. This fixes that.
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
    new_collection.page = Page.objects.get(
        user=request.user, name=page)
    new_collection.name = request.POST.get('collection_name').strip()
    new_collection.position = insert_at_position
    new_collection.save()

    return


def create_default_collection(request):
    """
    Add text.....
    """

    page = get_object_or_404(Page, user=request.user, position=1)

    page.collection_order_2 = [[1], []]
    page.collection_order_3 = [[1], [], []]
    page.collection_order_4 = [[1], [], [], []]
    page.collection_order_5 = [[1], [], [], [], []]
    page.save()

    new_collection = Collection()
    new_collection.user = request.user
    new_collection.page = Page.objects.get(
        user=request.user, name="Home")
    new_collection.name = "My First Collection"
    new_collection.position = 1
    new_collection.save()

    return


def delete_collection(request, page, collections):
    """
    Function to remove a collection from the db, and re-order
    position values to reflect the changes due to the deleted
    collection.

    Args:
        request (obj): The request object
        page (obj): The current page
        collections (queryset): Collections for current page and user
    """
    collection_to_delete = get_object_or_404(
        Collection,
        page__name=page.name,
        user=request.user,
        name=request.POST.get('collection')
    )
    position_to_delete = collection_to_delete.position
    collection_to_delete.delete()
    messages.success(
            request, f"Collection deletion successful.")

    # reset collection.position for each
    for count, collection in enumerate((collections), 1):
        collection.position = count
        collection.save()

    # reset column ordering numbers for each 2 through 5
    new_collection_orders = []
    for i in range(2, 6):
        collection_order = json.loads(
            eval('page.collection_order_'+str(i)))

        # find deleted position and remove from list
        for x in collection_order:
            if position_to_delete in x:
                x.remove(position_to_delete)

        # rename remaining positions starting from 1
        count = 1
        for col in range(len(collection_order)):
            for pos in range(len(collection_order[col])):
                collection_order[col][pos] = count
                count += 1

        new_collection_orders.append(collection_order)

    page.collection_order_2 = new_collection_orders[0]
    page.collection_order_3 = new_collection_orders[1]
    page.collection_order_4 = new_collection_orders[2]
    page.collection_order_5 = new_collection_orders[3]
    page.save()

    return
