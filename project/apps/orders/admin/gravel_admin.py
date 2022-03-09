from django.contrib import admin
from django.utils.html import format_html as fh
from simple_history.admin import SimpleHistoryAdmin as SHA
from apps.core.admin import deactivate, activate, get_change, get_history
from apps.orders.models import Gravel
from django.utils import timezone
from .admin_filters import OverdueFilter

@admin.register(Gravel)
class GravelAdmin(SHA):
    
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
        if request.user.is_superuser:
            return True
        return False
    
    list_display = [
        "po",
        "supplier",
        "progress",
        "job_site",
        "get_lots",
        "ndate",
        "get_history",
    ]
    history_list_display = ["changes"]
    
    list_filter = [
        "ndate",
        "ndate",
        "progress",
        "priority",
        "job_site",
        "bldr",
        "is_complete",
        OverdueFilter,
    ]

    actions = []

    fieldsets = (
        
        ("Location", {
            "fields": (
                "bldr",
                ("job_site", "lot",),
            ),
        }),
        ("Loads", {
            "fields": (
               "caller", 
               ("rloads","dloads",),
            ),
        }),
        ("Stone", {
            "fields": (
                "stype",
               ("bsdt","supplier","driver",),
            ),
        }),
        ("Dates", {
            "fields": (
                "odate",
                ("ndate","ddate",),
            ),
        }),
        (None, {
            "fields": (
                "priority",
                "po",
            ),
        }),
    )
    


