from bs4 import BeautifulSoup
from .conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

import itertools
import json
import requests as req

from premium.utils import is_premium
from .utils import page_utils, collection_utils, bookmark_utils
from .forms import (AddNewPageForm, EditPageForm, AddBookmarkForm,
                    EditBookmarkForm, MoveBookmarkForm)
from .models import Bookmark, Collection, Page


# views
def links(request, page):
    # check page exists, redirect if not
    try:
        page = Page.objects.get(user=request.user, name=page)
    except ObjectDoesNotExist:
        return redirect('links', page='qhome')  # qhome currently, to see errs

    collections = Collection.objects.filter(
        user__username=request.user,
        page__name=page.name
        ).order_by('position')

    bookmarks = Bookmark.objects.filter(
        user__username=request.user,
        collection__in=collections
        )

    # below moved up, before bookmarks - test this is ok
    # ------------------------------
    # collections = Collection.objects.filter(
    #     user__username=request.user,
    #     page__name=page.name
    #     ).order_by('position')

    # page forms
    add_new_page_form = AddNewPageForm(
        current_user=request.user, prefix='new_page', auto_id=False
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

        # if no pages left, create a default page & redirect to it
        if not Page.objects.filter(user=request.user).exists():
            page_utils.create_default_page(request)

        # redirect to first page
        page = Page.objects.get(user=request.user, position=1)
        return redirect('links', page=page)

    # add a new collection
    if 'add-collection' in request.POST:
        # check name is allowed and if so, add to db
        proposed_name = request.POST.get('collection_name')
        if collection_utils.validate_name(
                request, proposed_name, collections, page):
            collection_utils.add_collection(request, page)

        return redirect('links', page=page)

    # rename collection form
    if 'rename-collection-form' in request.POST:
        collection_position = request.POST.get('collection-position')
        proposed_name = request.POST.get('new-collection-name')

        if collection_utils.validate_name(
                request, proposed_name, collections, page):
            collection_to_rename = get_object_or_404(
                Collection, user=request.user,
                page=page,
                position=int(collection_position)
            )
            collection_to_rename.name = proposed_name
            collection_to_rename.save()
        return redirect('links', page=page)

    # delete collection
    if 'delete-collection-form' in request.POST:
        collection_utils.delete_collection(request, page, collections)
        return redirect('links', page=page)

    # delete bookmark
    if 'delete-bookmark-form' in request.POST:
        bookmark_utils.delete_bookmark(request)
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


def add_bookmark(request, page):

    try:
        page = Page.objects.get(user=request.user, name=page)
    except ObjectDoesNotExist:
        return redirect('links', page='qhome')  # qhome currently, to see errs

    add_bookmark_form = AddBookmarkForm(request.user, page)

    if 'add-bm-form' in request.POST:
        add_bookmark_form = AddBookmarkForm(request.user, page, request.POST)

        if add_bookmark_form.is_valid():
            form = add_bookmark_form.save(commit=False)

            form.user = request.user

            # set position value to next highest value. ie, last on list
            max_pos_value = Bookmark.objects.filter(
                user__username=request.user,
                collection__id=request.POST['collection']).aggregate(
                    Max('position')
            )

            form.position = 1 if not max_pos_value['position__max'] else \
                max_pos_value['position__max'] + 1

            if not form.description:
                form.description = "No description found"

            add_bookmark_form.save()

            return redirect('links', page=page)

    else:
        add_bookmark_form = AddBookmarkForm(request.user, page)

    # get page names for sidebar
    all_pages = Page.objects.filter(user=request.user).order_by('position')

    context = {"page": page.name,
               "all_page_names": all_pages,
               "add_bookmark_form": add_bookmark_form}
    context = is_premium(request.user, context)

    return render(request, 'links/add_bookmark.html', context)


def scrape_url(request):

    url = request.POST.get('urlToScrape', None)
    data = {'message': 'The URL is empty',
            'title': '',
            'description': ''}

    if not url:
        return JsonResponse(data)

    try:
        r = req.get(url)
        r.raise_for_status()

    except req.exceptions.RequestException:
        data['message'] = 'Could not load this URL'

    else:
        soup = BeautifulSoup(r.text, 'html.parser')
        scraped_title = soup.title.get_text()

        metas = soup.find_all('meta')
        for m in metas:
            if 'name' in m.attrs and m.attrs['name'] == 'description':
                scraped_description = m.attrs['content']

        try:
            scraped_description
        except UnboundLocalError:
            scraped_description = "Sorry, no metadata available for this URL"

        data = {'message': 'Success',
                'title': scraped_title,
                'description': scraped_description}

    return JsonResponse(data)


def edit_bookmark(request, page, bookmark):

    try:
        page = Page.objects.get(user=request.user, name=page)
    except ObjectDoesNotExist:
        return redirect('links', page='qhome')

    bookmark_to_edit = get_object_or_404(
        Bookmark, pk=bookmark
    )

    edit_bookmark_form = EditBookmarkForm(instance=bookmark_to_edit)

    if 'edit-bm-form' in request.POST:
        edit_bookmark_form = EditBookmarkForm(
            request.POST, instance=bookmark_to_edit)

        if edit_bookmark_form.is_valid():
            edit_bookmark_form.save()
            return redirect('links', page=page)

    # get page names for sidebar
    all_pages = Page.objects.filter(user=request.user).order_by('position')

    context = {"page": page.name,
               "bookmark": bookmark_to_edit,
               "edit_bookmark_form": edit_bookmark_form,
               "all_page_names": all_pages,
               }
    context = is_premium(request.user, context)

    return render(request, 'links/edit_bookmark.html', context)


def check_valid_url(request):

    url = request.POST.get('urlToCheck', None)
    data = {}

    if not url:
        return JsonResponse(data)

    try:
        response = req.head(url)
        response.raise_for_status()

    except req.exceptions.RequestException:
        data['result'] = False

    else:
        data['result'] = True

    return JsonResponse(data)


def move_bookmark(request, page, bookmark):

    try:
        page = Page.objects.get(user=request.user, name=page)
    except ObjectDoesNotExist:
        return redirect('links', page='qhome')

    try:
        bookmark_to_move = Bookmark.objects.get(user=request.user, pk=bookmark)
    except ObjectDoesNotExist:
        # stop users trying to move bookmarks that aren't theirs
        messages.error(
            request, f"That is not your bookmark to move!")
        return redirect('links', page=page)

    move_bookmark_form = MoveBookmarkForm(
        request.user, page, initial={'dest_page': page})

    if 'move-bm-form' in request.POST:
        orig_collection = bookmark_to_move.collection

        dest_collection = Collection.objects.get(
            id=request.POST.get('dest_collection'))

        # get new position value for bookmark
        dest_position = Bookmark.objects.filter(
            user=request.user, collection=dest_collection
        ).count() + 1

        # update bookmark object with new collection & position
        bookmark_to_move.collection = dest_collection
        bookmark_to_move.position = dest_position
        bookmark_to_move.save()

        # Reapply position values to bookmarks in the original collection
        # to account for the gap made when moving the bookmark out
        orig_collection_to_reorder = Bookmark.objects.filter(
            user=request.user, collection=orig_collection
        ).order_by('position')
        bookmark_utils.reorder_bookmarks(orig_collection_to_reorder)

        return redirect('links', page=page)

    # get page names for sidebar
    all_pages = Page.objects.filter(user=request.user).order_by('position')

    context = {"page": page.name,
               "bookmark": bookmark_to_move,
               "move_bookmark_form": move_bookmark_form,
               "all_page_names": all_pages,
               }
    context = is_premium(request.user, context)

    return render(request, 'links/move_bookmark.html', context)


def update_collection_list(request):
    """
    Get a page.id from POST and use it to generate html of collection
    names and values for the 'dest_collection' dropdown list.
    """

    new_page = get_object_or_404(
        Page, user=request.user, id=request.POST.get('newPagePk')
    )

    new_collections = Collection.objects.filter(
        user=request.user, page=new_page
    ).order_by('position')

    # build a dict of collection pk's and names
    new_collections_dict = {}
    for collection in new_collections:
        new_collections_dict[collection.pk] = collection

    # add the new collection data to an html string
    html = ''
    for k, v in new_collections_dict.items():
        html += f'<option value="{k}">{v}</option>'

    data = {'success': True, 'html': html}
    return JsonResponse(data)


def import_url(request):
    # check user is logged in
    print(request.user)
    if not request.user.is_authenticated:
        messages.error(
            request, f"You need to be logged in to add a bookmark")
        return redirect('about_page')

    context = {}
    context = is_premium(request.user, context)

    return render(request, 'links/import_url.html', context)
