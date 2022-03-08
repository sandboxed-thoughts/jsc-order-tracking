from django.contrib import admin
from django.utils.html import format_html as fh


@admin.display(description="deactivate selected")
def deactivate(self, request, queryset):
    queryset.update(is_active=False)


@admin.display(description="activate selected")
def activate(self, request, queryset):
    queryset.update(is_active=True)


def get_change(self, obj):
    # adds the field as "changed"
    # provides a dict with the changed value for future possibilities
    if obj.prev_record:
        chg = obj.diff_against(obj.prev_record)
        cfds = ""
        for c in chg.changes:
            cfds += "%(field)s from %(old)s to %(new)s<br/>" % {
                "field": " ".join(str(c.field).split("_")),
                "old": c.old,
                "new": c.new,
            }
        return fh(cfds)
    return "created"
