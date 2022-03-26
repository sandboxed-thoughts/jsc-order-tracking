from django.contrib import admin

from apps.core.admin import get_change, get_history
from apps.schedules.admin import GravelDeliveryInline
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import GravelOrder


@admin.register(GravelOrder)
class GravelOrderAdmin(SHA):
    class Media:
        # extra javascript
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "core/scripts/list_filter_collapse.js",
        ]

    list_display = ("po", "supplier", "lots", "priority", "nloads", "need_by", "get_history")
    list_filter = ("supplier", "lots", "item", "priority", "need_by")
    inlines = [
        GravelDeliveryInline,
    ]

    def changes(self, obj):
        return get_change(self, obj)

    def get_history(self, obj):
        return get_history(self, "orders", "gravelorder", obj)

    history_list_display = ["changes"]

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
