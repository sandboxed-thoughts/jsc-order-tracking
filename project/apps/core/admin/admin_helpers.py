from django.contrib import admin
from django.utils.html import format_html as fh


@admin.display(description="deactivate selected")
def deactivate(self, request, queryset):
    for inst in queryset:
        inst.is_active = False
        inst.save()


@admin.display(description="activate selected")
def activate(self, request, queryset):
    for inst in queryset:
        inst.is_active = True
        inst.save()
        inst.refresh_from_db()


@admin.display(description="history")
def get_history(self, cname, mname, obj):
    return fh(
        '<a href="/%(cname)s/%(mname)s/%(obj_id)s/history"><i class="fas fa-eye"></i></a>'
        % {
            "cname": cname,
            "mname": mname,
            "obj_id": obj.pk,
        }
    )


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
