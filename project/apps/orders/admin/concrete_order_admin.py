from django.contrib import admin

from apps.concrete.admin import ConcreteTypeInline
from apps.core.admin import get_change, get_history, save_note_inline
from apps.schedules.admin import PumpScheduleInline
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import ConcreteInspection, ConcreteOrder, ConcreteOrderNote, FlatworkItem, FootingsItem


class ConcreteOrderNoteInline(admin.TabularInline):
    model = ConcreteOrderNote
    extra = 0

    fields = ["author", "note", "updated_on"]
    readonly_fields = ["author", "updated_on"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            author_id = request.user.pk
            if author_id:
                kwargs["initial"] = author_id
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
        "id",
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

    def save_formset(self, request, form, formset, change):
        user = request.user
        instances = formset.save(commit=False)

        for instance in instances:
            if isinstance(instance, ConcreteOrderNote):  # Check if it is the correct type of inline
                save_note_inline(instance, user)
            else:
                instance.save()

        for obj in formset.deleted_objects:
            if isinstance(obj, ConcreteOrderNote):
                if any([user.is_superuser, user.groups.filter(name__in=("Administrators")), user.pk == obj.author_id]):
                    obj.delete()

            elif any([user.is_superuser, user.groups.filter(name__in=("Administrators"))]):
                obj.delete()
