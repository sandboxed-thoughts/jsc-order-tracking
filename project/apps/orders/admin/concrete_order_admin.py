from django.contrib import admin

from apps.core.admin import get_change, get_history, save_note_inline
# from apps.schedules.admin import PumpScheduleInline
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import ConcreteOrder, ConcreteOrderNote, ConcreteType, FlatworkItem, FootingsItem, PumpOrder


class ConcreteTypeInline(admin.StackedInline):
    """Stacked Inline View for ConcreteType"""

    model = ConcreteType
    min_num = 0
    max_num = 20
    extra = 0


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
        # PumpScheduleInline,
        # InspectionModelInline,
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
        "site__name",
        "builder__name",
        "needs_pump",
        "supplier",
        "dispatcher",
    ]

    date_hierarchy = "date_needed"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "po",
                    "builder",
                    "site",
                    "lots",
                    "needs_pump",
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
