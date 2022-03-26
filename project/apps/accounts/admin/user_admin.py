from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin, UserAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.utils.translation import gettext_lazy as _

from apps.core.admin.admin_helpers import activate, deactivate

from ..models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    actions = [activate, deactivate]

    ordering = ["email"]

    list_display = [
        "get_full_name",
        "email",
        "is_active",
    ]

    list_filter = [
        "is_active",
        "groups",
    ]

    history_list_display = ["changed"]

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

    check_groups = [
        "Administrators",
        "Project Managers",
    ]

    def get_queryset(self, request):
        """Only superusers can see superusers"""
        if not request.user.is_superuser:
            qs = self.model.editable_objects.get_queryset()
            ordering = self.ordering or ()
            if ordering:
                qs = qs.order_by(*ordering)
            return qs
        return super().get_queryset(request)

    def has_delete_permission(self, request, obj=None) -> bool:
        return True if request.user.is_superuser else False


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
