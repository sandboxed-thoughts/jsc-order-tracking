from django.contrib import admin
from django.utils.html import format_html as fh

from apps.core.admin import activate, deactivate, get_change, get_history
from simple_history.admin import SimpleHistoryAdmin as SHA

from .models import StoneType, ConcreteType, Supplier


@admin.register(StoneType)
class StoneTypeAdmin(admin.ModelAdmin):
    """Admin View for StoneType"""

    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(ConcreteType)
class ConcreteTypeAdmin(admin.ModelAdmin):
    """Admin View for ConcreteType"""

    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Supplier)
class SupplierAdmin(SHA):
    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == lookup,
                "query_string": cl.get_query_string(
                    {
                        self.parameter_name: lookup,
                    },
                    [],
                ),
                "display": title,
            }

    def queryset(self, request, queryset):
        if self.value() in ("activate", "rejected"):
            return queryset.filter(status=self.value())
        elif self.value() is None:
            return queryset.filter(status="pending")
        return queryset

    class Media:
        # extra javascript
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "core/scripts/list_filter_collapse.js",
        ]

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def changes(self, obj):
        return get_change(self, obj)

    def get_history(self, obj):
        return get_history(self, "jobs", "jobsite", obj)

    actions = [activate, deactivate]

    list_display = [
        "name",
        "is_active",
        "get_addr",
        "phone",
        "email",
        "get_site",
        "fax",
    ]

    search_fields = [
        "name",
        "street",
        "city",
        "state",
        "zip",
    ]

    list_filter = [
        "city",
        "is_active",
    ]

    history_list_display = ["changes"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "name",
                        "is_active",
                    ),
                    (
                        "phone",
                        "fax",
                    ),
                    (
                        "email",
                        "website",
                    ),
                    "street",
                    (
                        "city",
                        "state",
                        "zipcode",
                    ),
                ),
            },
        ),
    )
