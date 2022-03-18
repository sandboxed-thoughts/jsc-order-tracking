from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import ConcreteOrder, PumpSchedule, PumpScheduleNotes


class PumpScheduleNotesInline(admin.StackedInline):
    model = PumpScheduleNotes
    extra = 0


@admin.register(ConcreteOrder)
class ConcreteOrderAdmin(SHA):
    pass


@admin.register(PumpSchedule)
class PumpScheduleAdmin(SHA):
    inlines = [
        PumpScheduleNotesInline,
    ]
