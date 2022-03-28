from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import NoteModel
from simple_history.models import HistoricalRecords as HR

from .order_schedule_models import GravelDeliverySchedule, PumpSchedule

User = settings.AUTH_USER_MODEL


class PumpScheduleNote(NoteModel):

    pump = models.ForeignKey(
        PumpSchedule, verbose_name=_("pump"), related_name="pump_schedule", on_delete=models.CASCADE
    )

    def __str__(self):
        return "{0} [{1}]".format(self.pump.__str__(), self.pk)

    class Meta:
        db_table = "schedules_pump_schedule_notes"
        managed = True
        verbose_name = "Pump Schedule Note"
        verbose_name_plural = "Pump Schedule Notes"


class GravelDeliveryScheduleNote(NoteModel):

    delivery = models.ForeignKey(
        GravelDeliverySchedule, verbose_name=_("pump"), related_name="gravel_delivery", on_delete=models.CASCADE
    )

    def __str__(self):
        pass

    class Meta:
        db_table = "schedules_gravel_delivery_schedule_notes"
        managed = True
        verbose_name = "Gravel Delivery Note"
        verbose_name_plural = "Gravel Delivery Notes"
