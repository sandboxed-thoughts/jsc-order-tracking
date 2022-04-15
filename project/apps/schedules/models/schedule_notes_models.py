from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import NoteModel

from ..models import ConcreteOrderSchedule, GravelDeliverySchedule

User = settings.AUTH_USER_MODEL


class ConcreteOrderScheduleNote(NoteModel):

    pump = models.ForeignKey(
        ConcreteOrderSchedule, verbose_name=_("pump"), related_name="pump_schedule_notes", on_delete=models.CASCADE
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
        GravelDeliverySchedule, verbose_name=_("pump"), related_name="gravel_delivery_notes", on_delete=models.CASCADE
    )

    def __str__(self):
        return "{0} [{1}]".format(self.delivery.__str__(), self.pk)

    class Meta:
        db_table = "schedules_gravel_delivery_schedule_notes"
        managed = True
        verbose_name = "Gravel Delivery Note"
        verbose_name_plural = "Gravel Delivery Notes"
