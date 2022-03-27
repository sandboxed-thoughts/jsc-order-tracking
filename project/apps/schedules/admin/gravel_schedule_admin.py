from django.contrib import admin

from apps.core.admin import get_change, get_history
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..helpers import mark_complete
from ..models import GravelDeliverySchedule as GravelDelivery, GravelDeliveryScheduleNote


class GravelDeliveryScheduleNoteInline(admin.StackedInline):
    """Stacked Inline View for GravelDeliveryScheduleNote"""

    model = GravelDeliveryScheduleNote
    min_num = 0
    extra = 1


class GravelDeliveryInline(admin.TabularInline):
    """Tabular Inline View for GravelDelivery"""

    model = GravelDelivery
    min_num = 0
    max_num = 500
    extra = 0


@admin.register(GravelDelivery)
class GravelDeliveryAdmin(SHA):
    class Media:
        # extra javascript
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "core/scripts/list_filter_collapse.js",
        ]

    list_display = ("get_driver", "sdate", "order", "status", "loads", "get_history")
    list_filter = (
        "driver",
        "sdate",
        "status",
    )

    inlines = [
        GravelDeliveryScheduleNoteInline,
    ]

    actions = [mark_complete]

    def changes(self, obj):
        return get_change(self, obj)

    def get_history(self, obj):
        return get_history(self, "schedules", "graveldeliveryschedule", obj)

    history_list_display = ["changes"]

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def get_queryset(self, request):
        if not request.user.groups.filter(name__in=["Administrators", "Project Managers", "Dispatchers"]).exists():
            if request.user.groups.filter(name__in=["Drivers"]).exists():
                return super().get_queryset(request).filter(driver=request.user)
        return super().get_queryset(request)
