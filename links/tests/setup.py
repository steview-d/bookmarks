from links.models import Page, Collection, Bookmark
from links.utils.page_utils import build_empty_collection_order


# --------------------- SETUP ---------------------

def create_test_page():
    Page.objects.create(
        name="test_page",
        position=1,
        collection_order_2=build_empty_collection_order(2),
        collection_order_3=build_empty_collection_order(3),
        collection_order_4=build_empty_collection_order(4),
        collection_order_5=build_empty_collection_order(5),
        )


def create_test_collection():
    Collection.objects.create(
        name="test_collection",
        position=1,
    )


def create_test_bookmark():
    Bookmark.objects.create(
        url="https://www.google.com",
        title="Google",
        description="Search & Stuff",
        position=1,
    )


def create_test_url():
    test_url = "http://google.com"
    return test_url
