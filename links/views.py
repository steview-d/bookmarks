from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404

import copy
import json

from premium.utils import is_premium
from .utils import add_page
from .forms import AddNewPageForm
from .models import Bookmark, Collection, Page
# from .utils import change_num_columns


# Create your views here.
def links(request, page):
    # check page exists, redirect if not
    try:
        page = Page.objects.get(user=request.user, name=page)
    except ObjectDoesNotExist:
        return redirect('links', page='qhome')  # qhome currently, to see errs

    # forms
    add_new_page_form = AddNewPageForm(
        current_user=request.user
    )

    # add new page form
    if 'add-page-form' in request.POST:
        form_data = AddNewPageForm(request.POST, current_user=request.user)
        if form_data.is_valid():
            new_page = add_page(request, form_data)
            return redirect('links', page=new_page)

        else:
            add_new_page_form = form_data

    bookmarks = Bookmark.objects.filter(
        user__username=request.user
        )
    collections = Collection.objects.filter(
        user__username=request.user).filter(
        page__name=page.name
        )

    # create list of page names for sidebar
    all_page_names = []
    all_pages = Page.objects.filter(user=request.user)
    for name in all_pages:
        all_page_names.append(name.name)

    # generate collection names & order
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
            if collection_list[col] != []:
                for pos in range(len(collection_list[col])):
                    count += 1
                    collection_name = get_object_or_404(
                        Collection,
                        page__name=page.name,
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
                page__name=page.name,
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

    # # forms
    # add_new_page_form = AddNewPageForm()

    # set this page as the last page visited
    request.session['last_page'] = page.name

    # testing....

    context = {"column_width": 100 / num_of_columns,
               "num_of_columns": num_of_columns,
               "bm_data": bm_data,
               "page": page.name,
               "all_page_names": all_page_names,
               "add_new_page_form": add_new_page_form, }
    context = is_premium(request.user, context)

    return render(request, 'links/links.html', context)
