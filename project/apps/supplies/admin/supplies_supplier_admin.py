from django.contrib import admin
from django.utils.html import format_html as fh

from apps.core.admin import activate, deactivate, get_change, get_history
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import Supplier


@admin.register(Supplier)
class SupplierAdmin(SHA):

    actions = [
        activate,
        deactivate,
    ]

    list_display = [
        "name",
        "is_active",
        "has_gravel",
        "has_concrete",
        "has_pump",
        "get_addr",
        "phone",
        "email",
        "get_site",
        "fax",
        "get_history",
    ]

    search_fields = [
        "name",
        "street",
        "city",
        "state",
        "zip",
    ]

    list_filter = [
        "city",
        "is_active",
        "has_gravel",
        "has_concrete",
        "has_pump",
    ]

    history_list_display = ["changes"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "name",
                        "is_active",
                    ),
                    (
                        "has_gravel",
                        "has_pump",
                        "has_concrete",
                    ),
                    (
                        "phone",
                        "fax",
                    ),
                    (
                        "email",
                        "website",
                    ),
                    "street",
                    (
                        "city",
                        "state",
                        "zipcode",
                    ),
                ),
            },
        ),
    )

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def changes(self, obj):
        return get_change(self, obj)

    def get_history(self, obj):
        return get_history(self, "supplies", "supplier", obj)
