
from django.contrib import messages
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.models import User

from links.models import Page


def build_empty_collection_order(num):
    """
    Build a 2d list of empty lists, ready to hold collection
    position values

    Args:
        num (int): The number of lists to build inside the main list
    """
    empty_order = []
    for i in range(num):
        empty_order.append([])
    return empty_order


def add_page(request, form_data):
    """
    Build a new page and add to the db.

    Args:
        request (obj): The request object
        form_data (obj): The submitted form data
    """

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
    """
    Change the name of the requetsed form and save to the db.

    Args:
        request (obj): The request object
        new_page_name (str): The page name inputted by the user
        old_page_name (obj): The original / current page name
    """

    page = get_object_or_404(
        Page, user=request.user, name=old_page_name
    )
    page.name = new_page_name
    page.save()
    return new_page_name


def delete_page(request, page):
    """
    Delete the requested page and re-allocate page.position values
    to be 1 through [no' pages], in order.

    Args:
        request (obj): The request object
        page (obj): The current page
    """
    # delete page
    get_object_or_404(
        Page,
        name=page,
        user=request.user,
    ).delete()
    messages.success(
            request, f"Page Deletion Successful")

    # re-allocate .position values
    pages = Page.objects.filter(user=request.user).order_by('position')
    for count, page in enumerate((pages), 1):
        page.position = count
        page.save()

    return


def create_default_page(request):
    """
    A quick function to create a default page for the user called 'home'
    Used when a user logs in to the app for the first time, or if the user
    deletes all their pages
    """

    page = Page(user=request.user,
                name="home",
                position=1,
                collection_order_2=build_empty_collection_order(2),
                collection_order_3=build_empty_collection_order(3),
                collection_order_4=build_empty_collection_order(4),
                collection_order_5=build_empty_collection_order(5),
                )
    page.save()

    return redirect('links', page=page.name)
