from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import NoteModel


@admin.register(NoteModel)
class NoteModelAdmin(admin.ModelAdmin):
    """Admin View for NoteModel"""

    list_display = ("author",)
    list_filter = ("author", "created_on", "updated_on")
    search_fields = ("",)
    date_hierarchy = "updated_on"
    ordering = ("author", "-updated_on")

    class Media:
        css = {"all": ("css/base.css",)}
