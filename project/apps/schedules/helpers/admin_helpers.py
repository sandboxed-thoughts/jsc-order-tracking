from django.contrib import admin
from django.utils import timezone

# from django.utils.html import format_html as fh
from .choice_helpers import PourProgress, StatusChoices


@admin.display(description="Complete delivery")
def mark_complete(self, request, queryset):
    for inst in queryset:
        inst.status = StatusChoices.COMPLETE
        inst.ddate = timezone.localtime()
        inst.save()
        inst.refresh_from_db()


@admin.display(description="complete delivery")
def mark_pump_complete(self, request, queryset):
    for inst in queryset:
        inst.progress = PourProgress.COMPLETE
        inst.pdate = timezone.localdate()
        inst.ctime = timezone.localtime()
        inst.save()
        inst.refresh_from_db()
