from django.contrib import admin

from apps.core.admin import get_change, get_history
from apps.orders.models import Gravel
from simple_history.admin import SimpleHistoryAdmin as SHA
from apps.orders.models import Concrete




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
        if request.user.is_superuser:
            return True
        return False
