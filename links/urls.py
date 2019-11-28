from django.urls import path

from .views import links

urlpatterns = [
    path('', links, name="links"),
]
