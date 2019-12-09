from django.db.models import Max
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from links.models import Page


def add_page(request, form_data):
    """
    Build a new page record.
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
