from django.urls import path

from .views import (links, start_app, page_sort, arrange_collections,
                    collection_sort, add_bookmark, edit_bookmark,
                    move_bookmark, check_valid_url, update_collection_list,
                    import_url, manual_url_scrape, import_url_success,
                    bookmark_sort_manual, change_collection_display,
                    update_sort_order, custom_message)
# from .utils import start_app, change_num_columns
from .utils import collection_utils

urlpatterns = [
    path('start-app', start_app, name="start_app"),
    path('import-url/', import_url, name="import_url"),
    path('import-url-success/', import_url_success, name="import_url_success"),
    path('<page>/add-bookmark', add_bookmark, name="add_bookmark"),
    path('<page>/<bookmark>/edit-bookmark',
         edit_bookmark, name="edit_bookmark"),
    path('<page>/<bookmark>/move-bookmark',
         move_bookmark, name="move_bookmark"),
    path('update_collection_list',
         update_collection_list, name="update_collection_list"),
    path('<page>/<message>/custom_message',
         custom_message, name="custom_message"),
    path('change-num-columns/<page>/<num>',
         collection_utils.change_num_columns, name="change_num_columns"),
    path('<page>/<collection>/<sort>/update_sort_order',
         update_sort_order, name='update_sort_order'),
    path('page_sort', page_sort, name="page_sort"),
    path('bookmark_sort_manual',
         bookmark_sort_manual, name="bookmark_sort_manual"),
    path('change_collection_display',
         change_collection_display, name="change_collection_display"),
    path('check_valid_url', check_valid_url, name="check_valid_url"),
    path('manual_url_scrape', manual_url_scrape, name="manual_url_scrape"),
    path('<page>', links, name="links"),
    path('<page>/arrange',
         arrange_collections, name="arrange_collections"),
    path('<page>/collection-sort', collection_sort, name="collection_sort"),
]
