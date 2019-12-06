from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.models import User

from .models import Page


def start_app(request):
    """
    This function loads the app when coming from bm icon logo or after
    logging in. It will either point to page the last page visited,
    stored in session, or if no session value, it will load the page at
    position 1.
    """
    try:
        last_page = request.session['last_page']

    except KeyError:
        last_page = Page.objects.get(user=request.user, position=1)
        request.session['last_page'] = last_page.name

    return redirect('links', page=last_page)


def change_num_columns(request, page, num):
    if int(num) > 0 and int(num) < 6:
        page = get_object_or_404(
            Page, user=request.user, name=page
        )
        page.num_of_columns = num
        page.save()
    return redirect('links', page=page.name)


def add_page(request, form_data):
    """
    Use this to build a new page.
    Needs to not only create a new page object, but also
    configure it so it has all required default info so it
    can display ok, for instance
    - Name, position, column order lists, etc
    """

    print("ALL VALID")
    form = form_data.save(commit=False)
    form.name = form.name.lower()
    form.user = User.objects.get(username=request.user)

    # set position to next highest value, so last on list
    max_pos_value = Page.objects.filter(
        user__username=request.user).aggregate(
            Max('position')
    )
    form.position = max_pos_value['position__max'] + 1

    # set empty collection order values
    form.collection_order_2 = build_empty_collection_order(2)
    form.collection_order_3 = build_empty_collection_order(3)
    form.collection_order_4 = build_empty_collection_order(4)
    form.collection_order_5 = build_empty_collection_order(5)

    form.save()

    new_page = form.name
    return new_page


def edit_page_name(request, new_page_name, old_page_name):
    # form = form_data.save(commit=False)
    # name = form.name
    page = get_object_or_404(
        Page, user=request.user, name=old_page_name
    )
    page.name = new_page_name
    page.save()
    return new_page_name


def build_empty_collection_order(num):
    """
    Build a 2d list of empty lists, ready to hold collection
    position values
    """
    empty_order = []
    for i in range(num):
        empty_order.append([])
    return empty_order
