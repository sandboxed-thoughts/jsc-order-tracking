from django.contrib import admin
from django.utils.timezone import now

# from django.utils.html import format_html as fh
from .choice_helpers import StatusChoices, PourProgress


@admin.display(description="Complete delivery")
def mark_complete(self, request, queryset):
    for inst in queryset:
        inst.status = StatusChoices.COMPLETE
        inst.ddate = now()
        inst.save()
        inst.refresh_from_db()


@admin.display(description="complete delivery")
def mark_pump_complete(self, request, queryset):
    for inst in queryset:
        inst.progress = PourProgress.COMPLETE
        inst.pdate = now().date()
        inst.ctime = now().time()
        inst.save()
        inst.refresh_from_db()
