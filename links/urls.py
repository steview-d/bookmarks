from django.urls import path

from .views import links
from .utils import start_app, change_num_columns

urlpatterns = [
    path('start_app', start_app, name="start_app"),
    path('change_num_columns/<page>/<num>', change_num_columns,
         name="change_num_columns"),
    path('<page>', links, name="links")
]
