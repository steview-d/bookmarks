from .conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect, render

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
        # 1000 is an arbitrary value. Can be any number that is higher
        # than the maximum amount of bm's that will be stored
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


def collection_sort(request):
    qdata = request.POST.get('new_collection_order', None)
    print("DATA: ", qdata)

    # do magic

    data = {'success': True}
    return JsonResponse(data)
