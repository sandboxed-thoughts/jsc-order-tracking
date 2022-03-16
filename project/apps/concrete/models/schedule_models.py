from lib2to3.pgen2 import driver

from django.conf import settings
from django.db import models
from django.forms import MultipleChoiceField
from django.utils.translation import gettext_lazy as _

from apps.core.models import NoteModel
from simple_history.models import HistoricalRecords as HR

from ..helpers import PourProgress

User = settings.AUTH_USER_MODEL


class PumpSchedule(models.Model):
    """
    Model for storing a schedule of all concrete pump jobs

    fields:
        project_manager (int):  ForeignKey -> User
        operator (int):         ForeignKey  -> User
        crew (str):             CharField
        pdate (date):           DateField
        ctime (datetime):       DateTimeField
        loads (float):          FloatField
        progress (str):         CharField
    """

    project_manager = models.ForeignKey(
        User, verbose_name=_("project manager"), related_name="pm_pump_schedule", on_delete=models.CASCADE
    )
    driver = models.ForeignKey(
        User, verbose_name=_("operator"), related_name="driver_pump_schedule", on_delete=models.CASCADE
    )
    crew = models.CharField(_("crew pouring"), max_length=150, blank=True, null=True)
    pdate = models.DateField(_("pour date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    ctime = models.TimeField(_("concrete time"), auto_now=False, auto_now_add=False, blank=True, null=True)
    loads = models.FloatField(_("loads"), default=0)
    progress = models.CharField(
        _("pump progress"), choices=PourProgress.choices, default=PourProgress.WILL_CALL, max_length=11
    )
    history = HR()

    class Meta:
        db_table = "concrete_schedule"
        managed = True
        verbose_name = "pump schedule"


class ScheduleNotes(NoteModel):
    """schedule notes"""

    pump = models.ForeignKey(
        "PumpSchedule", verbose_name=_("pump scheduled"), related_name="pump_notes", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return "{} {}".format(self.author, self.pump.pdate)

    class Meta:
        db_table = "concrete_schedule_notes"
        managed = True
        verbose_name = "note"
        verbose_name_plural = "notes"


class InclimateWeather(models.Model):
    """Records a delay in the pump schedule

    fields:
        pump (int):     ForeignKey -> PumpSchedule
        temp (str):     CharField
        precip (str):   CharField
    """

    pump = models.ForeignKey("PumpSchedule", verbose_name=_("inclimate weather"), on_delete=models.CASCADE)
    temp = models.CharField(_("temperature"), max_length=50)
    precip = models.CharField(_("precipitation"), max_length=50)
    history = HR()

    class Meta:
        db_table = "concrete_schedule_weather"
        managed = True
        verbose_name = "inclimate weather report"
        verbose_name_plural = "inclimate weather reports"


class WeatherNotes(NoteModel):
    "notes on inclimate weather"

    weather = models.ForeignKey(
        "InclimateWeather", verbose_name=_("weather note"), related_name="weather_notes", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return "{} {}".format(self.author, self.delay)

    class Meta:
        db_table = "concrete_schedule_weather_notes"
        managed = True
        verbose_name = "note"
