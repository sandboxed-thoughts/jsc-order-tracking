from django.contrib import admin

from apps.concrete.admin import ConcreteTypeInline
from apps.core.admin import get_change, get_history
from apps.schedules.admin import PumpScheduleInline
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import ConcreteInspection, ConcreteOrder, ConcreteOrderNote, FlatworkItem, FootingsItem


class ConcreteOrderNoteInline(admin.StackedInline):
    model = ConcreteOrderNote
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            author = request.user
            if author:
                kwargs["initial"] = author
        return super(ConcreteOrderNoteInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class InspectionModelInline(admin.StackedInline):
    model = ConcreteInspection
    extra = 0
    verbose_name = "Inspection"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "agent",
                    ("phone", "fax"),
                    "email",
                    "inspection_date",
                    "note",
                ),
            },
        ),
    )


class FootingsItemInline(admin.StackedInline):
    model = FootingsItem
    extra = 0


class FlatworkItemInline(admin.StackedInline):
    model = FlatworkItem
    extra = 0


@admin.register(ConcreteOrder)
class ConcreteOrderAdmin(SHA):
    class Media:
        css = {"all": ("core/css/base.css",)}

    inlines = [
        ConcreteTypeInline,
        FlatworkItemInline,
        FootingsItemInline,
        ConcreteOrderNoteInline,
        PumpScheduleInline,
        InspectionModelInline,
    ]

    list_select_related = True

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
        "get_history",
        "get_notes",
    ]

    list_filter = [
        "site",
        "builder",
        "supplier",
        "dispatcher",
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
