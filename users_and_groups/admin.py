from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from users_and_groups.models import User, Group


class CustomUserAdmin(UserAdmin):
    model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add field 'patr' to user in admin panel and reorder
        self.fieldsets[1][1]['fields'] = ("last_name", "first_name", "patr", "email")


class CustomGroupAdmin(GroupAdmin):
    pass


admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)

admin.site.unregister(DjangoGroup)
