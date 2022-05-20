from django.contrib import admin

from apps.core.admin import get_change, get_history, save_note_inline
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import PumpOrder, PumpOrderNote


class PumpOrderNoteInline(admin.TabularInline):
    model = PumpOrderNote
    extra = 0

    fields = ["author", "note", "updated_on"]
    readonly_fields = ["author", "updated_on"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            author = request.user
            if author:
                kwargs["initial"] = author
        return super(PumpOrderNoteInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(PumpOrder)
class PumpOrderAdmin(SHA):
    """Admin for Pump Orders (Pump Rentals)"""

    list_display = [
        "__str__",
        "builder",
        "site",
        "concrete_order",
        "pump_supplier",
        "created_on",
    ]

    inlines = [
        PumpOrderNoteInline,
    ]

    def changes(self, obj):
        return get_change(self, obj)

    def get_history(self, obj):
        return get_history(self, "orders", "gravelorder", obj)

    history_list_display = ["changes"]

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def save_formset(self, request, form, formset, change):
        user = request.user
        instances = formset.save(commit=False)

        for instance in instances:
            if isinstance(instance, PumpOrderNote):  # Check if it is the correct type of inline
                save_note_inline(instance, user)
            else:
                instance.save()

        for obj in formset.deleted_objects:
            if isinstance(obj, PumpOrderNote):
                if any([user.is_superuser, user.groups.filter(name__in=("Administrators")), user.pk == obj.author_id]):
                    obj.delete()

                elif any([user.is_superuser, user.groups.filter(name__in=("Administrators"))]):
                    obj.delete()
