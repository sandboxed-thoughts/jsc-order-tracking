from django.contrib import admin
from django.utils.html import format_html as fh
from simple_history.admin import SimpleHistoryAdmin as SHA
from .models import JobSite
from apps.core.admin import deactivate, activate, get_change, get_history


@admin.register(JobSite)
class JobSiteAdmin(SHA):
    class Media:
        # extra javascript
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "core/scripts/list_filter_collapse.js",
        ]

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def changes(self, obj):
        return get_change(self, obj)

    def get_history(self, obj):
        return get_history(self, "jobs", "jobsite", obj)

    actions = [activate, deactivate]

    search_fields = [
        "name",
        "street",
        "city",
        "state",
        "zipcode",
    ]

    list_filter = [
        "city",
        "is_active",
    ]

    list_display = [
        "name",
        "get_addr",
        "is_active",
        "get_history",
    ]

    history_list_display = ["changes"]
    exclude = ["change_reason"]


    fieldsets = (
        (None, {
            "fields": (
                ("name", "is_active",),
                "street",
                ("city", "state","zipcode"),
            ),
        }),        
    )
    
    