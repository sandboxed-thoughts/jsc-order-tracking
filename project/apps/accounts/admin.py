from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin, UserAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.utils.html import format_html as fh
from django.utils.translation import gettext_lazy as _

from apps.core.admin import activate, deactivate, get_change
from simple_history.admin import SimpleHistoryAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, SimpleHistoryAdmin):
    class Media:
        # extra javascript
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "core/js/list_filter_collapse.js",
        ]

    @admin.display(description="history")
    def get_history(self, obj):
        return fh(
            "<a href='/accounts/customuser/%(obj_id)s/history'>view history</a>"
            % {
                "obj_id": obj.pk,
            }
        )

    def changes(self, obj):
        return get_change(self, obj)

    actions = [activate, deactivate]
    ordering = ["email"]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "get_history",
    ]
    list_filter = [
        "is_active",
        "groups",
    ]
    history_list_display = ["changes"]
    fieldsets = (
        (
            None,
            {
                "fields": ("email", "password", ("first_name", "last_name")),
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_active", "groups"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    ("password1", "password2"),
                    ("first_name", "last_name"),
                    "groups",
                ),
            },
        ),
    )


class Group(DjangoGroup):
    """Instead of trying to get new user under existing `Aunthentication and Authorization`
    banner, create a proxy group model under our Accounts app label.
    Refer to: https://github.com/tmm/django-username-email/blob/master/cuser/admin.py
    """

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")
        proxy = True


admin.site.unregister(DjangoGroup)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass
