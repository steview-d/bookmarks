from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .utils import is_premium

# Create your views here.
@login_required
def premium(request):

    context = {}
    context = is_premium(request.user, context)

    return render(request, 'premium/premium.html', context)
