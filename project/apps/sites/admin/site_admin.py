from django.contrib import admin

from apps.core.admin import activate, deactivate, get_change, get_history, save_note_inline
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import SiteModel, SiteNote


class SiteNoteInline(admin.StackedInline):
    model = SiteNote
    extra = 0

    fields = ['author', 'note', 'updated_on']
    readonly_fields = ['author', 'updated_on']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            author_id = request.user.pk
            if author_id:
                kwargs["initial"] = author_id
        return super(SiteNoteInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(SiteModel)
class SiteModelAdmin(SHA):

    inlines = [
        SiteNoteInline,
    ]

    list_display = (
        "site_name",
        "get_addr",
        "is_active",
        "get_history",
        "get_notes",
    )
    list_filter = (
        "city",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "project_manager",
                    "site_name",
                ),
            },
        ),
        (
            "Address",
            {
                "fields": (("city", "state", "zipcode"),),
            },
        ),
    )
    actions = [
        activate,
        deactivate,
    ]

    def changes(self, obj):
        return get_change(self, obj)

    def get_history(self, obj):
        return get_history(self, "sites", "sitemodel", obj)

    history_list_display = ["changes"]

    def save_formset(self, request, form, formset, change):
        user = request.user
        instances = formset.save(commit=False)

        for instance in instances:
            if isinstance(instance, SiteNote):  # Check if it is the correct type of inline
                save_note_inline(instance, user)
            else:
                instance.save()

        for obj in formset.deleted_objects:
            if isinstance(obj, SiteNote):
                if any([user.is_superuser, user.groups.filter(name__in=("Administrators")), user.pk == obj.author_id]):
                    obj.delete()

            elif any([user.is_superuser, user.groups.filter(name__in=("Administrators"))]):
                obj.delete()
