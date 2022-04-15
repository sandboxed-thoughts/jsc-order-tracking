from lib2to3.pgen2 import driver

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import NoteModel
from simple_history.models import HistoricalRecords as HR

from ..models import ConcreteOrderSchedule

User = settings.AUTH_USER_MODEL


class InclimateWeather(models.Model):
    """Records a delay in the pump schedule

    fields:
        pump (int):     ForeignKey -> PumpSchedule
        temp (str):     CharField
        precip (str):   CharField
    """

    pump = models.ForeignKey(
        ConcreteOrderSchedule, verbose_name=_("pump schedule"), related_name="pump_delay", on_delete=models.CASCADE
    )
    temp = models.CharField(_("temperature"), max_length=50)
    precip = models.CharField(_("precipitation"), max_length=50)
    history = HR()

    def str(self):
        return "delay {0}".format(self.pk)

    class Meta:
        db_table = "schedules_concrete_schedule_weather"
        managed = True
        verbose_name = "inclimate weather report"
        verbose_name_plural = "inclimate weather reports"


class InclimateWeatherNote(NoteModel):
    """note for InclimateWeather"""

    delay = models.ForeignKey(InclimateWeather, verbose_name=_("delay"), on_delete=models.CASCADE)
