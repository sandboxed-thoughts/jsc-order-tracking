from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin as SHA
from ..models import (PumpSchedule, PumpScheduleNotes, InclimateWeather,)


class PumpScheduleNotesInline(admin.StackedInline):
    model = PumpScheduleNotes
    extra = 0


class InclimateWeatherInline(admin.StackedInline):
    model = InclimateWeather
    extra = 0
    min_num = 0


@admin.register(PumpSchedule)
class PumpScheduleAdmin(SHA):
    inlines = [
        PumpScheduleNotesInline,
        InclimateWeatherInline,
    ]
    list_display = [
        "driver",
        "crew",
        "pdate",
        "loads",
        "progress",
    ]
    list_filter = [
        "driver",
        "pdate",
        "progress",
    ]