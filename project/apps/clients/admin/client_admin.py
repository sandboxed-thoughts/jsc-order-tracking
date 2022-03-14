from django.contrib import admin

from apps.core.admin import activate, deactivate, get_change, get_history
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import Builder, Lot, Subdivision


class LotInline(admin.TabularInline):
    """Stacked Inline View for Lot"""

    model = Lot
    min_num = 0
    max_num = 20
    extra = 0


@admin.register(Builder)
class BuilderAdmin(SHA):
    list_display = (
        "name",
        "get_addr",
        "phone",
        "email",
        "is_active",
        "get_history",
    )
    list_filter = (
        "city",
        "is_active",
    )
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
    inlines = [
        LotInline,
    ]

    def changes(self, obj):
        return get_change(self, obj)

    def get_history(self, obj):
        return get_history(self, "clients", "builder", obj)

    history_list_display = ["changes"]


@admin.register(Subdivision)
class SubdivisionAdmin(SHA):
    list_display = (
        "name",
        "get_addr",
        "is_active",
        "get_history",
    )
    list_filter = (
        "city",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": ("name",),
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
        return get_history(self, "clients", "subdivision", obj)

    history_list_display = ["changes"]

    inlines = [
        LotInline,
    ]


# not registered
class LotAdmin(SHA):
    list_display = (
        "name",
        "builder",
        "subdivision",
        "get_history",
    )
    list_filter = ("builder", "subdivision")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "name",
                        "builder",
                        "subdivision",
                    ),
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
        return get_history(self, "clients", "lot", obj)

    history_list_display = ["changes"]
