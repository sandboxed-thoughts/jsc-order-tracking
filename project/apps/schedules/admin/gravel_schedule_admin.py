from django.contrib import admin

from apps.core.admin import get_change, get_history, save_note_inline
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..helpers import mark_complete
from ..models import GravelDeliverySchedule as GravelDelivery, GravelDeliveryScheduleNote


class GravelDeliveryScheduleNoteInline(admin.TabularInline):
    """Stacked Inline View for GravelDeliveryScheduleNote"""

    fields = ["author", "note", "updated_on"]
    readonly_fields = ["author", "updated_on"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            author_id = request.user.pk
            if author_id:
                kwargs["initial"] = author_id
        return super(GravelDeliveryScheduleNoteInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    model = GravelDeliveryScheduleNote
    min_num = 0
    extra = 0


class GravelDeliveryInline(admin.StackedInline):
    """Tabular Inline View for GravelDelivery"""

    model = GravelDelivery
    min_num = 0
    max_num = 500
    extra = 0


@admin.register(GravelDelivery)
class GravelDeliveryAdmin(SHA):
    class Media:
        css = {"all": ("core/css/base.css",)}
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "core/scripts/list_filter_collapse.js",
        ]

    list_display = (
        "order",
        "status",
        "order_builder",
        "order_supplier",
        "order_lots",
        "get_driver",
        "sdate",
        "order_item",
        "loads",
        "ddate",
        "get_history",
        "get_notes",
    )
    list_filter = (
        "driver",
        "status",
        "order__builder",
        "order__supplier",
        "order__item",
    )

    inlines = [
        GravelDeliveryScheduleNoteInline,
    ]

    actions = [mark_complete]

    def changes(self, obj):
        return get_change(self, obj)

    @admin.display(description="History")
    def get_history(self, obj):
        return get_history(self, "schedules", "graveldeliveryschedule", obj)

    history_list_display = ["changes"]

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def get_queryset(self, request):
        if not request.user.groups.filter(name__in=["Administrators", "Project Managers", "Dispatchers"]).exists():
            if request.user.groups.filter(name__in=["Drivers"]).exists():
                return super().get_queryset(request).filter(driver=request.user)
        return super().get_queryset(request)

    def save_formset(self, request, form, formset, change):
        user = request.user
        instances = formset.save(commit=False)

        for instance in instances:
            if isinstance(instance, GravelDeliveryScheduleNote):  # Check if it is the correct type of inline
                save_note_inline(instance, user)
            else:
                instance.save()

        for obj in formset.deleted_objects:
            if isinstance(obj, GravelDeliveryScheduleNote):
                if any([user.is_superuser, user.groups.filter(name__in=("Administrators")), user.pk == obj.author_id]):
                    obj.delete()

            elif any([user.is_superuser, user.groups.filter(name__in=("Administrators"))]):
                obj.delete()
