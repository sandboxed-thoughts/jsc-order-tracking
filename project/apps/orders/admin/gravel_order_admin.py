from django.contrib import admin

from apps.core.admin import get_change, get_history, save_note_inline

# from apps.schedules.admin import GravelDeliveryInline
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import GravelOrder, GravelOrderNote


class GravelOrderNoteInline(admin.TabularInline):
    model = GravelOrderNote
    extra = 0

    fields = ["author", "note", "updated_on"]
    readonly_fields = ["author", "updated_on"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            author = request.user
            if author:
                kwargs["initial"] = author
        return super(GravelOrderNoteInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(GravelOrder)
class GravelOrderAdmin(SHA):
    class Media:
        css = {"all": ("core/css/base.css",)}

    list_select_related = True
    list_display = [
        "pk",
        "status",
        "builder",
        "site",
        "get_lots",
        "priority",
        "nloads",
        "need_by",
        "po",
        "supplier",
        "get_history",
        "get_notes",
    ]
    list_filter = [
        "status",
        "priority",
        "builder__name",
        "site__name",
    ]
    search_fields = [
        "supplier__name",
        "builder__name",
        "site__site_name",
        "lots",
        "po",
    ]
    date_hierarchy = 'need_by'
    inlines = [
        GravelOrderNoteInline,
        # GravelDeliveryInline,
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
            if isinstance(instance, GravelOrderNoteInline):  # Check if it is the correct type of inline
                save_note_inline(instance, user)
            else:
                instance.save()

        for obj in formset.deleted_objects:
            if isinstance(obj, GravelOrderNoteInline):
                if any([user.is_superuser, user.groups.filter(name__in=("Administrators")), user.pk == obj.author_id]):
                    obj.delete()

                elif any([user.is_superuser, user.groups.filter(name__in=("Administrators"))]):
                    obj.delete()
