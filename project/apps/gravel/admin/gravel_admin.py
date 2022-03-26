from django.contrib import admin

from apps.core.admin import get_change, get_history
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import StoneType


@admin.register(StoneType)
class StoneTypeAdmin(admin.ModelAdmin):
    """Admin View for StoneType"""

    class Media:
        # extra javascript
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "core/scripts/list_filter_collapse.js",
        ]

    list_display = ("name", "description")
    search_fields = ("name", "description")

    def changes(self, obj):
        return get_change(self, obj)

    def get_history(self, obj):
        return get_history(self, "gravel", "gravelorder", obj)

    history_list_display = ["changes"]

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
