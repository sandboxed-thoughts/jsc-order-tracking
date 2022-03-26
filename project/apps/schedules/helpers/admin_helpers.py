from django.contrib import admin
from django.utils.timezone import datetime

# from django.utils.html import format_html as fh
from .choice_helpers import StatusChoices


@admin.display(description="Complete delivery")
def mark_complete(self, request, queryset):
    for inst in queryset:
        inst.status = StatusChoices.COMPLETE
        inst.ddate = datetime.now()
        inst.save()
        inst.refresh_from_db()
