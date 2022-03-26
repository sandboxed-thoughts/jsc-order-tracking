from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.orders.models import GravelOrder
from simple_history.models import HistoricalRecords as HR

from ..helpers import PourProgress, StatusChoices

User = settings.AUTH_USER_MODEL


class GravelDeliverySchedule(models.Model):
    """delivery schedule of a gravel order

    Args:
        order   (str):      ForeignKey -> GravelOrder
        ddriver (int):      ForeignKey -> AUTH_USER_MODEL
        sdate   (datetime): DateField
        loads   (int):      SmallIntegerField
        note    (str):      ForeignKey -> NoteModel
        status  (str):      CharField -> StatusChoices

    Returns:
        _type_: _description_
    """

    order = models.ForeignKey(GravelOrder, verbose_name=_("order"), on_delete=models.PROTECT)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("delivery driver"),
        related_name="deliveries",
        limit_choices_to={"groups__name": "Drivers"},
        on_delete=models.PROTECT,
    )
    sdate = models.DateField(_("scheduled for"), auto_now=False, auto_now_add=False, default=timezone.now)
    loads = models.SmallIntegerField(_("loads"), default=1)
    status = models.CharField(
        _("status"), max_length=11, choices=StatusChoices.choices, default=StatusChoices.SCHEDULED
    )
    ddate = models.DateTimeField(_("delivered on"), auto_now=False, auto_now_add=False, blank=True, null=True)
    history = HR()

    def __str__(self) -> str:
        """label for class instance

        Returns:
            str: first letter of first name, full last name, instance pk
        """
        return "{0}. {1} [{2}]".format(self.driver.first_name[0].capitalize(), self.driver.last_name.title(), self.pk)

    def save(self, *args, **kwargs):

        super(GravelDeliverySchedule, self).save(*args, **kwargs)  # Call the real save() method

    class Meta:
        db_table = "orders_gravel_deliveries"
        managed = True
        verbose_name = "Gravel Delivery"
        verbose_name_plural = "Gravel Deliveries"
        ordering = ["-sdate", "driver"]


class PumpSchedule(models.Model):
    """
    Model for storing a schedule of all concrete pump jobs

    fields:
        driver (int):         ForeignKey  -> User
        crew (str):             CharField
        pdate (date):           DateField
        ctime (datetime):       DateTimeField
        loads (float):          FloatField
        progress (str):         CharField
    """

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("delivery driver"),
        related_name="pump_schedules",
        limit_choices_to={"groups__name": "Drivers"},
        on_delete=models.PROTECT,
    )
    crew = models.CharField(_("crew pouring"), max_length=150, blank=True, null=True)
    pdate = models.DateField(_("pour date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    ctime = models.TimeField(_("concrete time"), auto_now=False, auto_now_add=False, blank=True, null=True)
    loads = models.FloatField(_("loads"), default=0)
    progress = models.CharField(
        _("pump progress"), choices=PourProgress.choices, default=PourProgress.WILL_CALL, max_length=11
    )
    order = models.ForeignKey(
        "orders.ConcreteOrder",
        verbose_name=_("concrete order"),
        related_name="pump_schedule",
        on_delete=models.CASCADE,
    )
    history = HR()

    class Meta:
        db_table = "concrete_pump_schedule"
        managed = True
        verbose_name = "concrete pump schedule"
