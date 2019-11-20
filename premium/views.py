from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render

from .utils import is_premium

# Create your views here.
@login_required
def premium(request):
    if request.method == "POST":
        print("OPOP")
        premium_group = Group.objects.get(name='Premium')
        user = User.objects.get(email=request.user.email)
        user.groups.add(premium_group)

    context = {}
    context = is_premium(request.user, context)

    return render(request, 'premium/premium.html', context)
