from django.contrib import admin
from django.utils.html import format_html as fh
from simple_history.admin import SimpleHistoryAdmin as SHA
from .models import JobSite
from apps.core.admin import deactivate, activate, get_change


@admin.register(JobSite)
class JobSiteAdmin(SHA):
    @admin.display(description="address")
    def full_address(self):
        return self.get_addr()

    class Media:
        # extra javascript
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "core/scripts/list_filter_collapse.js",
        ]

        actions = [activate, deactivate]

        list_filter = [
            "name",
            "city",
            "is_active",
        ]

        list_display = [
            "name",
            "full_address",
            "is_active",
        ]
