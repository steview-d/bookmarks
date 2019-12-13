from django.urls import path

from .views import links, page_sort
# from .utils import start_app, change_num_columns
from .utils import general_utils, collection_utils

urlpatterns = [
    path('start_app', general_utils.start_app, name="start_app"),
    path('change_num_columns/<page>/<num>',
         collection_utils.change_num_columns,
         name="change_num_columns"),
    path('page_sort', page_sort, name="page_sort"),
    path('<page>', links, name="links")
]
