from django.contrib import admin
from django.utils.html import format_html as fh
from simple_history.admin import SimpleHistoryAdmin as SHA
from orders.models import Gravel


@admin.register(Gravel)
class GravelAdmin(SHA):
    class Media:
        # extra javascript
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "core/scripts/list_filter_collapse.js",
        ]

    @admin.display(description="history")
    def get_history(self, obj):
        return fh("<a href='/orders/gravel/{}/history'>view history</a>".format(obj.pk))

    def changed(self, obj):
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
        return None

    list_display = [
        "po",
        "job_site",
        "lot",
        "n_date",
        "priority",
        "supplier",
        "stone",
        "get_history",
    ]
    history_list_display = ["changed"]
    list_filter = [
        "job_site",
        "lot",
        "n_date",
        "priority",
        "supplier",
        "stone",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("bldr", "job_site", "lot"),
                    "caller",
                    ("r_loads", "d_loads"),
                    "stone", 
                    "bsdt",
                    ("supplier", "driver"),
                    ("n_date", "d_date"),
                    "priority",
                    "po",
                ),
            },
        ),
    )
