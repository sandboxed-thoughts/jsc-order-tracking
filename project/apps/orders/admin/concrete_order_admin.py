from django.contrib import admin
from apps.core.admin import get_change, get_history
from apps.concrete.admin import ConcreteTypeInline
from apps.schedules.admin import PumpScheduleInline
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import ConcreteOrder, ConcreteOrderNote, FlatworkItem, FootingsItem, InspectionModel


class ConcreteOrderNoteInline(admin.StackedInline):
    model = ConcreteOrderNote
    extra = 0


class InspectionModelInline(admin.StackedInline):
    model = InspectionModel
    extra = 0


class FootingsItemInline(admin.StackedInline):
    model = FootingsItem
    extra = 0


class FlatworkItemInline(admin.StackedInline):
    model = FlatworkItem
    extra = 0


@admin.register(ConcreteOrder)
class ConcreteOrderAdmin(SHA):

    inlines = [
        ConcreteTypeInline,
        FlatworkItemInline,
        FootingsItemInline,
        ConcreteOrderNoteInline,
        PumpScheduleInline,
    ]

    list_display = [
        "po",
        "builder",
        "site",
        "get_lots",
        "supplier",
        "dispatcher",
        "get_ctypes",
        "etotal",
        "qordered",
        "date_needed",
        "get_notes",
        "get_history",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "po",
                    "builder",
                    "site",
                    "lots",
                    "supplier",
                    "dispatcher",
                    "etotal",
                    "atotal",
                    "qordered",
                    "date_needed",
                ),
            },
        ),
    )

    def changes(self, obj):
        return get_change(self, obj)

    def get_history(self, obj):
        return get_history(self, "orders", "concreteorder", obj)

    history_list_display = ["changes"]
