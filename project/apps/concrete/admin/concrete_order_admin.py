from django.contrib import admin
from ..models import ConcreteOrder, PumpSchedule
from simple_history.admin import SimpleHistoryAdmin as SHA


@admin.register(ConcreteOrder)
class ConcreteOrderAdmin(SHA):
    pass


@admin.register(PumpSchedule)
class PumpScheduleAdmin(SHA):
    pass
