from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    # get membership status
    def membership_status(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return "Premium" if "Premium" in groups else "Standard"

    list_display = (
        'username', 'email', 'date_joined', 'membership_status'
    )

    list_filter = ['groups', 'is_staff', 'is_superuser', 'is_active']

    ordering = ('-id',)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
