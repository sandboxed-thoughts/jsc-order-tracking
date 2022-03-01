from django.contrib import admin
from django.utils.html import format_html as fh
from django.db import models
from simple_history.admin import SimpleHistoryAdmin as SHA
from orders.models import Concrete


@admin.register(Concrete)
class ConcreteAdmin(SHA):
    class Media:
        # extra javascript
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "core/scripts/list_filter_collapse.js",
        ]

    @admin.display(description="history")
    def get_history(self, obj):
        return fh(
            "<a href='/orders/concrete/{}/history'>view history</a>".format(obj.pk)
        )

    def changed(self, obj):
        # adds the field and new data to the history list as "changed"
        if obj.prev_record:
            cfs = {}
            chg = obj.diff_against(obj.prev_record)
            for f in chg.changed_fields:
                cfs[str(obj._meta.get_field(f).verbose_name)] = str(
                    obj._meta.get_field(f).value_from_object(obj)
                )
            cfds = ""
            for k, v in cfs.items():
                cfds += "{0} to {1}<br>".format(k, v)
            return fh(cfds)
        return "Added"

    def lots(self, obj):
        return obj.get_lots()

    list_display = [
        "bldr",
        "job_site",
        "lots",
        "cpour",
        "supplier",
        "ono",
        "notes",
        "get_history",
    ]
    list_filter = [
        "job_site",
        "supplier",
        "otype",
        "bldr",
        "cpour",
        "pdate",
        "itime",
        "ctime",
        "pprog",
        "pump",
    ]
    search_fields = [
        "otype",
        "bldr",
        "job_site",
        "supplier",
        "notes",
        "dsph",
        "ono",
    ]
    history_list_display = ["changed"]

    fieldsets = (
        (
            "locations",
            {
                "fields": (
                    (
                        "bldr",
                        "job_site",
                        "lot",
                    ),
                ),
            },
        ),
        (
            "task info",
            {
                "fields": (
                    "pdate",
                    "otype",
                    "item",
                    (
                        "garage",
                        "wea",
                    ),
                ),
            },
        ),
        (
            "concrete supplier",
            {
                "fields": (
                    (
                        "ctype",
                        "ono"
                    ),
                    "supplier",
                    "dsph",
                ),
            },
        ),
        (
            "quantities",
            {
                "fields": (
                    ("etot","qord","atot",),
                ),
            },
        ),
        (
            "pump info",
            {
                "fields": (
                    "pump",
                    "cpour",
                    "pinfo",
                ),
            },
        ),
        (
            "inspections",
            {
                "fields": ("itime","iagt"),
            },
        ),
        (
            "pour progress",
            {
                "fields": (
                    ("temp","incw",),
                    "pprog","ctime",
                    
                ),
            },
        ),
        (
            "Additional Information", {
                "fields": ("notes",)
            }
        ),
    )

    radio_fields = {
        "incw": admin.HORIZONTAL,
        "temp": admin.HORIZONTAL,
        "otype": admin.HORIZONTAL,
        "ctype": admin.HORIZONTAL,
    }