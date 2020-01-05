from django.urls import path

from .views import (links, page_sort, arrange_collections, collection_sort,
                    add_bookmark, edit_bookmark, check_valid_url)
# from .utils import start_app, change_num_columns
from .utils import general_utils, collection_utils

urlpatterns = [
    path('start-app', general_utils.start_app, name="start_app"),
    path('<page>/add-bookmark', add_bookmark, name="add_bookmark"),
    path('<page>/<bookmark>/edit-bookmark',
         edit_bookmark, name="edit_bookmark"),
    path('change-num-columns/<page>/<num>',
         collection_utils.change_num_columns,
         name="change_num_columns"),
    path('page-sort', page_sort, name="page_sort"),
    path('check_valid_url', check_valid_url, name="check_valid_url"),
    path('<page>', links, name="links"),
    path('<page>/arrange',
         arrange_collections,
         name="arrange_collections"),
    path('<page>/collection-sort', collection_sort, name="collection_sort"),
]
