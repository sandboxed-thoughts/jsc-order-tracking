from django.contrib import admin
from django.utils.html import format_html as fh
from simple_history.admin import SimpleHistoryAdmin as SHA
from orders.models import Concrete, ConcreteNote


class CNoteInline(admin.StackedInline):
    model = ConcreteNote
    min_num = 1
    max_num = 1


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

    @admin.display(description="lots")
    def lots(self, obj):
        return obj.get_lots()

    list_display = [
        "otype",
        "pdate",
        "bldr",
        "job_site",
        "get_lots",
        "cpour",
        "supplier",
        "ono",
        "itime",
        "ctime",
        "pprog",
        "get_history",
    ]
    list_filter = [
        "otype",
        "job_site",
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
        "dsph",
        "ono",
    ]
    history_list_display = ["changed"]

    inlines = [
        CNoteInline,
    ]

    fieldsets = (
        (
            "locations",
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
            "task info",
            {
                "fields": (
                    (
                        "otype",
                        "pdate",
                    ),
                    (
                        "lot",
                        "item",
                    ),
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
                        "supplier",
                        "dsph",
                        "ono",
                    ),
                ),
            },
        ),
        (
            "quantities",
            {
                "fields": (
                    (
                        "etot",
                        "qord",
                        "atot",
                    ),
                    "ctype",
                ),
            },
        ),
        (
            "pump info",
            {
                "fields": (
                    "pump",
                    (
                        "pinfo",
                        "cpour",
                    ),
                ),
            },
        ),
        (
            "inspections",
            {
                "fields": (
                    (
                        "itime",
                        "iagt",
                    ),
                ),
            },
        ),
        (
            "pour progress",
            {
                "fields": (
                    (
                        "ctime",
                        "pprog",
                    ),
                    (
                        "incw",
                        "temp",
                    ),
                ),
            },
        ),
    )
