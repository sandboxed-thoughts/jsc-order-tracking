from django.contrib import admin

from apps.core.admin import get_change, get_history
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import GravelDelivery, GravelOrder

class GravelDeliveryInline(admin.TabularInline):
    '''Tabular Inline View for GravelDelivery'''

    model = GravelDelivery
    min_num = 1
    max_num = 500
    extra = 0
    
@admin.register(GravelOrder)
class GravelOrderAdmin(SHA):
    class Media:
        # extra javascript
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "core/scripts/list_filter_collapse.js",
        ]
    list_display = ('po','supplier','lot','priority','nloads','need_by')
    list_filter = ('supplier','lot','item','priority','need_by')
    inlines = [GravelDeliveryInline,]

    def changes(self, obj):
        return get_change(self, obj)

    def get_history(self, obj):
        return get_history(self, "gravel", "gravelorder", obj)

    history_list_display = ["changes"]

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

@admin.register(GravelDelivery)
class GravelDelivery(SHA):

    class Media:
        # extra javascript
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "core/scripts/list_filter_collapse.js",
        ]
    list_display = ('ddriver','sdate','order','status','notes','loads')
    list_filter = ('ddriver','sdate','status')

    def changes(self, obj):
        return get_change(self, obj)

    def get_history(self, obj):
        return get_history(self, "gravel", "gravelorder", obj)

    history_list_display = ["changes"]

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
