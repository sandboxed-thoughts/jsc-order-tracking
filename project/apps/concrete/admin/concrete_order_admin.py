from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import ConcreteOrder, PumpSchedule, ScheduleNotes


class ScheduleNotesInline(admin.StackedInline):
    model = ScheduleNotes
    extra = 0


@admin.register(ConcreteOrder)
class ConcreteOrderAdmin(SHA):
    pass


@admin.register(PumpSchedule)
class PumpScheduleAdmin(SHA):
    inlines = [
        ScheduleNotesInline,
    ]
