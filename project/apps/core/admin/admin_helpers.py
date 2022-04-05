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


@admin.display(description="", empty_value="")
def get_notes(notes):
    """Returns a formated string of notes to display on the admin list_display

        This function manipulates the list_display to hide the column get_notes sits in and inserts it as a new row.

    Args:
        notes (queryset): a list of notes for the model

    Returns:
        str:    <tr><td>Notes:</td><td colspan='5'>{0}</td></tr>".format(pnl)
                    if any notes for the model exists, return the formatted list of notes from earlierst to newest created
                    otherwise, return an empty string
    """

    nl = ['{0}:&ensp;"{1}"'.format(x.author, x.note) for x in notes.order_by("created_on")]
    if len(nl) > 0:
        pnl = "<br>".join(nl)
        return fh("<tr><td>Notes:</td><td colspan='5'>{0}</td></tr>".format(pnl))
    return ""


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


def save_note_inline(instance, user_id):
    if not instance.author_id:
        instance.author_id = user_id
    if instance.author_id and instance.author_id != user_id:
        return ValueError("you cannot edit another user's note")
    instance.save()
