from django.urls import path

from .views import links
from .utils import change_num_columns

urlpatterns = [
    path('', links, name="links"),
    path('change_num_columns/<page>/<num>', change_num_columns,
         name="change_num_columns")
]
