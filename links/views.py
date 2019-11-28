from django.shortcuts import render

from premium.utils import is_premium
from .models import Bookmark, Collection


# Create your views here.
def links(request):

    collections = Collection.objects.filter(user__username=request.user)
    collection_names = []
    for collection in collections:
        collection_names.append(collection.name)

    coll_dict = {}

    for i in range(len(collection_names)):
        qs = Bookmark.objects.filter(
            collection__name=collection_names[i]).order_by('position')
        coll_dict[collection_names[i]] = qs

    # for k, v in coll_dict.items():
    #     print(k, v)

    context = {'collections': coll_dict}
    context = is_premium(request.user, context)

    return render(request, 'links/links.html', context)
