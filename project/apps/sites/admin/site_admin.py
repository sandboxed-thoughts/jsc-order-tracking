from django.contrib import admin

from apps.core.admin import activate, deactivate, get_change, get_history
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import SiteModel, SiteNote


class SiteNoteInline(admin.StackedInline):
    model = SiteNote
    extra = 0


@admin.register(SiteModel)
class SiteModelAdmin(SHA):

    inlines = [
        SiteNoteInline,
    ]

    list_display = (
        "site_name",
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
                "fields": (
                    "project_manager",
                    "site_name",
                ),
            },
        ),
        (
            "Address",
            {
                "fields": (("city", "state", "zipcode"),),
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
        return get_history(self, "sites", "sitemodel", obj)

    history_list_display = ["changes"]
