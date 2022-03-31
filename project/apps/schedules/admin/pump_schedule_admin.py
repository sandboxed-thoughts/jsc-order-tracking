from django.contrib import admin

from apps.core.admin import get_change, get_history
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..helpers import mark_pump_complete
from ..models import InclimateWeather, InclimateWeatherNote, PumpSchedule, PumpScheduleNote


class PumpScheduleNotesInline(admin.StackedInline):
    model = PumpScheduleNote
    extra = 0


class InclimateWeatherNoteInline(admin.StackedInline):
    """Stacked Inline View for InclimateWeatherNote"""

    model = InclimateWeatherNote
    min_num = 0
    max_num = 20
    extra = 0


class InclimateWeatherInline(admin.StackedInline):
    model = InclimateWeather
    extra = 0
    min_num = 0


class PumpScheduleInline(admin.StackedInline):
    """Stacked Inline View for PumpSchedule"""

    model = PumpSchedule
    min_num = 0
    extra = 0


@admin.register(PumpSchedule)
class PumpScheduleAdmin(SHA):
    inlines = [
        PumpScheduleNotesInline,
        InclimateWeatherInline,
    ]
    list_display = [
        "__str__",
        "get_builder",
        "get_supplier",
        "get_driver",
        "get_site",
        "get_lots",
        "crew",
        "pdate",
        "ctime",
        "loads",
        "progress",
        "get_history",
    ]
    list_filter = [
        "driver",
        "pdate",
        "progress",
    ]

    actions = [mark_pump_complete]

    def changes(self, obj):
        return get_change(self, obj)

    @admin.display(description="schedule history")
    def get_history(self, obj):
        return get_history(self, "schedules", "pumpschedule", obj)

    @admin.display(description="builder")
    def get_builder(self, obj):
        return obj.order.builder.name

    @admin.display(description="supplier")
    def get_supplier(self, obj):
        return obj.order.supplier.name

    @admin.display(description="lots")
    def get_lots(self, obj):
        return obj.order.get_lots()

    @admin.display(description="site")
    def get_site(self, obj):
        return obj.order.site

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
