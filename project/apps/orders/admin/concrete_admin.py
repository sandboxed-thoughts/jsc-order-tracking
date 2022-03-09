from django.contrib import admin
from django.utils.html import format_html as fh
from apps.core.admin import get_change, get_history
from apps.orders.models import Concrete
from simple_history.admin import SimpleHistoryAdmin as SHA
from .admin_filters import OverdueFilter


@admin.register(Concrete)
class ConcreteAdmin(SHA):
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
        return get_history(self, "orders", "gravel", obj)

    def has_delete_permission(self, request, obj=None):
        """Turn off delete for all but superusers"""
        if request.user.is_superuser:
            return True
        return False

    @admin.display(description="Pour Area (ft)")
    def get_area(self, obj):
        """Consilidates garage and wea into one column"""
        if obj.otype == "footings":
            g = obj.garage
            w = obj.wea
            return fh("garage: {0}<br>'walkout: {1}".format(obj.garage, obj.wea))
        return "N/A"

    @admin.display(description="Ordered")
    def get_ordered(self, obj):
        """Consolidates the ordered amount and quanitity into one column"""
        return "{0} {1}".format(obj.qord, obj.qtype)

    @admin.display(description="Ordered")
    def get_estimated(self, obj):
        """Consolidates the estimated amount and quanitity into one column"""
        return "{0} {1}".format(obj.etot, obj.qtype)

    list_display = [
        "supplier",
        "dsph",
        "po",
        "otype",
        "job_site",
        "get_lots",
        "get_area",
        "get_estimated",
        "get_ordered",
    ]

    history_list_display = ["changes"]

    list_filter = [
        "supplier",
        "otype",
        "job_site",
        OverdueFilter,
    ]

    fieldsets = (
        (
            "Location",
            {
                "fields": (
                    (
                        "bldr",
                        "job_site",
                    ),
                ),
            },
        ),
        (
            "Task Info",
            {
                "fields": (
                    (
                        "lot",
                        "ctype",
                    ),
                ),
            },
        ),
        (
            "Concrete Supplier",
            {
                "fields": (
                    ("supplier", "dsph"),
                    "po",
                ),
            },
        ),
        (
            "Quantities",
            {
                "fields": (
                    (
                        "qtype",
                        "etot",
                    ),
                    (
                        "qord",
                        "atot",
                    ),
                )
            },
        ),
        (
            "Pump Info",
            {
                "fields": (
                    "pump",
                    "pinfo",
                    (
                        "progress",
                        "crew",
                    ),
                ),
            },
        ),
        (
            "Inspections",
            {
                "fields": (
                    (
                        "iagt",
                        "itime",
                    ),
                ),
            },
        ),
        (
            "Delays",
            {
                "fields": (
                    "incw",
                    "temp",
                ),
            },
        ),
    )
