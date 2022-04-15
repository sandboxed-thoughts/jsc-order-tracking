from django.contrib import admin

from apps.core.admin import get_change, get_history, save_note_inline
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..helpers import mark_pump_complete
from ..models import InclimateWeather, InclimateWeatherNote, ConcreteOrderSchedule, ConcreteOrderScheduleNote


class ConcreteOrderScheduleNotesInline(admin.TabularInline):
    model = ConcreteOrderScheduleNote
    extra = 0

    fields = ["author", "note", "updated_on"]
    readonly_fields = ["author", "updated_on"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            author_id = request.user.pk
            if author_id:
                kwargs["initial"] = author_id
        return super(ConcreteOrderScheduleNotesInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class InclimateWeatherNoteInline(admin.StackedInline):
    """Stacked Inline View for InclimateWeatherNote"""

    model = InclimateWeatherNote
    min_num = 0
    max_num = 20
    extra = 0


class InclimateWeatherInline(admin.StackedInline):
    model = InclimateWeather
    extra = 0
    min_num = 0


class ConcreteOrderScheduleInline(admin.StackedInline):
    """Stacked Inline View for PumpSchedule"""

    model = ConcreteOrderSchedule
    min_num = 0
    extra = 0


@admin.register(ConcreteOrderSchedule)
class ConcreteOrderScheduleAdmin(SHA):
    inlines = [
        ConcreteOrderScheduleNotesInline,
        InclimateWeatherInline,
    ]
    list_display = [
        "__str__",
        "get_builder",
        "get_supplier",
        "get_driver",
        "get_site",
        "get_lots",
        "crew",
        "pdate",
        "ctime",
        "loads",
        "progress",
        "get_history",
        "get_notes",
    ]
    list_filter = [
        "driver",
        "progress",
        "order__builder",
        "order__supplier",
    ]

    actions = [mark_pump_complete]

    def changes(self, obj):
        return get_change(self, obj)

    @admin.display(description="schedule history")
    def get_history(self, obj):
        return get_history(self, "schedules", "pumpschedule", obj)

    @admin.display(description="builder")
    def get_builder(self, obj):
        return obj.order.builder.name

    @admin.display(description="supplier")
    def get_supplier(self, obj):
        if not obj.order.supplier:
            return "None"
        return obj.order.supplier.name

    @admin.display(description="lots")
    def get_lots(self, obj):
        return obj.order.get_lots()

    @admin.display(description="site")
    def get_site(self, obj):
        return obj.order.site

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

    class Media:
        css = {"all": ("core/css/base.css",)}

    def save_formset(self, request, form, formset, change):
        user = request.user
        instances = formset.save(commit=False)

        for instance in instances:
            if isinstance(instance, ConcreteOrderScheduleNote):  # Check if it is the correct type of inline
                save_note_inline(instance, user)
            else:
                instance.save()

        for obj in formset.deleted_objects:
            if isinstance(obj, ConcreteOrderScheduleNote):
                if any([user.is_superuser, user.groups.filter(name__in=("Administrators")), user.pk == obj.author_id]):
                    obj.delete()

            elif any([user.is_superuser, user.groups.filter(name__in=("Administrators"))]):
                obj.delete()
