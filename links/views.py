from .conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect, render

import itertools
import json

from premium.utils import is_premium
from .utils import page_utils, collection_utils
from .forms import AddNewPageForm, EditPageForm
from .models import Bookmark, Collection, Page


# views
def links(request, page):
    # check page exists, redirect if not
    try:
        page = Page.objects.get(user=request.user, name=page)
    except ObjectDoesNotExist:
        return redirect('links', page='qhome')  # qhome currently, to see errs

    bookmarks = Bookmark.objects.filter(
        user__username=request.user
        )
    collections = Collection.objects.filter(
        user__username=request.user).filter(
        page__name=page.name
        ).order_by('position')

    # page forms
    add_new_page_form = AddNewPageForm(
        current_user=request.user
    )

    edit_page_form = EditPageForm(
        current_user=request.user
    )

    # add new page form
    if 'add-page-form' in request.POST:
        form_data = AddNewPageForm(request.POST, current_user=request.user)
        if form_data.is_valid():
            new_page = page_utils.add_page(request, form_data)
            return redirect('links', page=new_page)

        else:
            add_new_page_form = form_data

    # edit page form
    if 'edit-page-form' in request.POST:
        form_data = EditPageForm(request.POST, current_user=request.user)
        if form_data.is_valid():
            new_page_name = form_data.cleaned_data.get('name')
            name = page_utils.edit_page_name(request, new_page_name, page)
            return redirect('links', page=name)

        else:
            edit_page_form = form_data

    # delete page form
    if 'delete-page-form' in request.POST:
        page_utils.delete_page(request, page)
        return redirect('links', page='home')

    # add a new collection
    if 'add-collection' in request.POST:
        # check name is allowed and if so, add to db
        if collection_utils.validate_name(request, collections, page):
            collection_utils.add_collection(request, page)

        return redirect('links', page=page)

    # delete collection
    if 'delete-collection-form' in request.POST:
        collection_utils.delete_collection(request, page, collections)
        return redirect('links', page=page)

    # get page names for sidebar
    all_pages = Page.objects.filter(user=request.user).order_by('position')

    # generate collection names & order
    num_of_columns = page.num_of_columns
    collection_list = collection_utils.make_collection_list(
        request, page, num_of_columns, collections)

    # iterate through collection names and create a qs of bookmarks for each
    bm_data = []
    for x in range(num_of_columns):
        column = {}
        for j in (collection_list[x]):
            qs = bookmarks.filter(collection__name=j).order_by('position')
            column[j] = qs
        bm_data.append(column)

    # set this page as the last page visited
    request.session['last_page'] = page.name

    context = {"column_width": 100 / num_of_columns,
               "num_of_columns": num_of_columns,
               "bm_data": bm_data,
               "page": page.name,
               "all_page_names": all_pages,
               "add_new_page_form": add_new_page_form,
               "edit_page_form": edit_page_form, }
    context = is_premium(request.user, context)

    return render(request, 'links/links.html', context)


def page_sort(request):
    # get and format new page order
    data = request.POST.get('new_page_order', None)
    new_order = list(map(int, data.split(',')))

    old_page_order = Page.objects.filter(
        user=request.user).order_by('position')

    page_limit = settings.LINKS_PREM_MAX_PAGES

    # re-order pages based on user sort
    for idx, page in enumerate((old_page_order), 1):
        page.position_temp = new_order.index(page.position) + 1
        page.position = idx + page_limit
        page.save()

    for page in old_page_order:
        page.position = page.position_temp
        page.position_temp = None
        page.save()

    data = {'success': True}
    return JsonResponse(data)


def arrange_collections(request, page):
    try:
        page = Page.objects.get(user=request.user, name=page)
    except ObjectDoesNotExist:
        return redirect('links', page='qhome')  # qhome currently, to see errs

    collections = Collection.objects.filter(
        user__username=request.user).filter(
        page__name=page.name
        ).order_by('position')

    # get page names for sidebar
    all_pages = Page.objects.filter(user=request.user).order_by('position')

    num_of_columns = page.num_of_columns

    # generate collection names & order
    collection_list = collection_utils.make_collection_list(
        request, page, num_of_columns, collections)

    context = {"page": page.name,
               "num_of_columns": num_of_columns,
               "column_width": 100 / num_of_columns,
               "all_page_names": all_pages,
               "collection_data": collection_list, }
    context = is_premium(request.user, context)

    return render(request, 'links/arrange_collections.html', context)


def collection_sort(request, page):
    # get the page object
    try:
        page = Page.objects.get(user=request.user, name=page)
    except ObjectDoesNotExist:
        return redirect('links', page='qhome')

    # get collections
    collections = Collection.objects.filter(
        user__username=request.user).filter(
        page__name=page.name
        ).order_by('position')

    post_data = request.POST.get('new_collection_order', None)
    jdata = json.loads(post_data)

    # convert posted data to a list in same format as collection_order_[i]
    raw_collection_order = []
    for x in range(len(jdata)):
        raw_collection_order.append(jdata[x].split(','))
        for y in range(len(raw_collection_order[x])):
            if raw_collection_order[x][y] != '':
                raw_collection_order[x][y] = int(raw_collection_order[x][y])
            else:
                raw_collection_order[x].pop(y)

    # flatten raw collection order
    flattened_raw = list(itertools.chain(*raw_collection_order))

    # update page positions for items inside of collection
    for idx, i in enumerate((collections), 1):
        i.position = flattened_raw.index(idx) + 1
        i.save()

    # get collection / element number that is being moved
    collection_to_move = int((
        request.POST.get('collection_id', None)).replace('_.', ''))

    # to identify which column a collection should move to, use 'dest_contains'
    # this picks a collection in the destination column, so when moving a
    # collection, it's target will be the column containing this collection.
    empty_column_num = 0
    for col in range(len(raw_collection_order)):
        if collection_to_move in raw_collection_order[col]:
            dest_contains_list = raw_collection_order[col]
            # if destination column is empty (the 1 is the item being moved in)
            if len(dest_contains_list) == 1:
                dest_contains = 0
                empty_column_num = col + 1
            # store a collection number from destination column for the
            # collection being moved. This allows us to iterate through
            # columns, looking for this collection, and when found, put
            # the collection being moved into the same column.
            elif dest_contains_list[0] != collection_to_move:
                dest_contains = dest_contains_list[0]
            else:
                dest_contains = dest_contains_list[1]

    # update all collection_order_[i] fields
    new_collection_orders = []
    for i in range(2, 6):
        collection_order = json.loads(
            eval('page.collection_order_'+str(i)))

        # remove 'collection_to_move' from current position
        for col in range(len(collection_order)):
            if collection_to_move in collection_order[col]:
                collection_order[col].remove(collection_to_move)

        # if moving to an already populated column
        if dest_contains:
            for col in range(len(collection_order)):
                if dest_contains in collection_order[col]:
                    collection_order[col].append(collection_to_move)
        else:
            # insert collection into blank column
            insert_position = i if empty_column_num > i else empty_column_num
            collection_order[insert_position - 1].append(collection_to_move)

        # sort all collection_order_[i] lists into 1-n order
        count = 1
        for col in range(len(collection_order)):
            for pos in range(len(collection_order[col])):
                collection_order[col][pos] = count
                count += 1

        new_collection_orders.append(collection_order)

    # # save new page collection orders to db
    page.collection_order_2 = new_collection_orders[0]
    page.collection_order_3 = new_collection_orders[1]
    page.collection_order_4 = new_collection_orders[2]
    page.collection_order_5 = new_collection_orders[3]
    page.save()

    data = {'success': True}
    return JsonResponse(data)

    # TODO
    # Move most of code into collection utils, then see if can refactor
    # and DRY with other functions

    # TODO
    # Add ability to rename collections

    # TODO
    # Currently, collections seem to bunch to the right, will be something
    # to do with bit of code where I work from right to left if adding to
    # a colum which doesn't exist (add collections code / view).
    # To fix, maybe split it so it adds some to left if a certain condition
    # is met?

    # NOTE
    # To fix empty column bug, if moving to an empty column, identify the
    # empty column number. Then, for each collection_order_[i] move the
    # collection to the empty column, UNLESS that column does not exist, in
    # which case, add it to the end of the next available column, working
    # over from the right.
