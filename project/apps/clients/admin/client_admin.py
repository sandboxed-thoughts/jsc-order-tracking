from django.contrib import admin

from apps.core.admin import activate, deactivate, get_change, get_history
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import Client


@admin.register(Client)
class BuilderAdmin(SHA):
    class Media:
        css = {"all": ("core/css/base.css",)}

    list_display = [
        "name",
        "get_addr",
        "phone",
        "email",
        "is_active",
        "get_history",
    ]
    list_filter = [
        "city",
        "is_active",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": ("name",),
            },
        ),
        (
            "Contact Information",
            {
                "fields": (("email", "phone", "fax"),),
            },
        ),
        (
            "Address",
            {
                "fields": (
                    "street",
                    ("city", "state", "zipcode"),
                ),
            },
        ),
    )
    actions = [
        activate,
        deactivate,
    ]

    def changes(self, obj):
        return get_change(self, obj)

    def get_history(self, obj):
        return get_history(self, "clients", "client", obj)

    history_list_display = ["changes"]
