from django.contrib import admin
from django.utils.html import format_html as fh
from simple_history.admin import SimpleHistoryAdmin as SHA
from .models import ConcreteOrder

@admin.register(ConcreteOrder)
class ConcreteOrderAdmin(SHA):
    
    def get_history(self, obj):
        return fh("<a href='/concrete/concreteorder/{}/history'>view history</a>".format(obj.pk))
    get_history.short_description = "history"
    
    def changed(self, obj):
        if obj.prev_record:
            cfs = {}
            chg = obj.diff_against(obj.prev_record)
            for f in chg.changed_fields:
                cfs[str(obj._meta.get_field(f).verbose_name)] = str(obj._meta.get_field(f).value_from_object(obj))
            cfds = ""
            for k, v in cfs.items():
                cfds += "{0} to {1}<br>".format(k, v)
            return fh(cfds)
        return None

    # def get_lots(self):
        

    list_display = [
        'otype',
        'pdate',
        'bldr',
        'job_site',
        'lot',
        'cpour',
        'supplier',
        'ono',
        'itime',
        'ctime',
        'pprog',
        'get_history',
    ]
    list_filter = [
        'otype',
        'job_site',
        'bldr',
        'cpour',
        'pdate',
        'itime',
        'ctime',
        'pprog',
        'pump',
    ]
    search_fields = [
        "otype",
        "bldr",
        "job_site",
        "supplier",
        "dsph",
        "ono",
    ]
    history_list_display = ['changed']

    fieldsets = (
        ("locations", {
            "fields": (
                ("bldr",
                "job_site",),
            ),
        }),
        ("task info", {
            "fields": (
                ("otype",
                 "pdate",),
                ("lot",
                "item",),
                ("garage",
                 "wea",),
            ),
        }),
        ("concrete supplier", {
            "fields": (
                ("supplier",
                "dsph",
                "ono",),
            ),
        }),
        ("quantities", {
            "fields": (
            ("etot",
                "qord",
                "atot",),
                "ctype",
            ),
        }),
        ("pump info", {
            "fields": (
                "pump",
                ("pinfo",
                "cpour",),
            ),
        }),
        ("inspections", {
            "fields": (
                ("itime",
                "iagt",),
            ),
        }),
        ("pour progress", {
            "fields": (
                ("ctime",
                "pprog",),
                ("incw",
                "temp",),
            ),
    }),
)
