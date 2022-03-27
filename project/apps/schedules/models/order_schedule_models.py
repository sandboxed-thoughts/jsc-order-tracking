from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.orders.models import GravelOrder, ConcreteOrder
from simple_history.models import HistoricalRecords as HR

from ..helpers import PourProgress, StatusChoices

User = settings.AUTH_USER_MODEL


class GravelDeliverySchedule(models.Model):
    """delivery schedule of a gravel order

    Args:
        order               (str):          ForeignKey -> GravelOrder
        supplier_delivers   (bool):         BooleanField
        driver              (int):          ForeignKey -> AUTH_USER_MODEL
        sdate               (datetime):     DateField
        loads               (int):          SmallIntegerField
        status              (str):          CharField -> StatusChoices
        ddate               (datetime):     DateTimeField
        get_driver          (str):          returns the driver's full name or the supplier if supplier_delivers
    """

    order = models.ForeignKey(
        GravelOrder, verbose_name=_("order"), related_name="gravel_deliveries", on_delete=models.PROTECT
    )
    supplier_delivers = models.BooleanField(
        _("supplier delivers"),
        default=False,
        help_text="Check if the supplier is responsible for delivering the order",
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("delivery driver"),
        related_name="deliveries",
        limit_choices_to={"groups__name": "Drivers"},
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    sdate = models.DateField(_("scheduled for"), auto_now=False, auto_now_add=False, default=timezone.now)
    loads = models.SmallIntegerField(_("loads"), default=1)
    status = models.CharField(
        _("status"), max_length=11, choices=StatusChoices.choices, default=StatusChoices.SCHEDULED
    )
    ddate = models.DateTimeField(_("delivered on"), auto_now=False, auto_now_add=False, blank=True, null=True)
    history = HR()

    @admin.display(description="delivery driver")
    def get_driver(self):
        """if supplier_delivers return supplier name, otherwise return the driver's full name"""

        if self.supplier_delivers:
            return self.order.supplier.name
        return self.driver.get_full_name()

    def __str__(self) -> str:
        """label for class instance

        Returns:
            str: first letter of first name, full last name, instance pk
        """
        return "{0} [{1}]".format(self.get_driver(), self.pk)

    def clean(self):
        """
        Require at least one of supplier_delivers or driver to be set - but not both
        """
        if not (self.supplier_delivers or self.driver):
            raise ValidationError(
                {
                    "supplier_delivers": ValidationError(_("Someone must deliver the order.")),
                    "driver": ValidationError(_("Someone must deliver the order.")),
                }
            )

        if self.supplier_delivers and self.driver:
            raise ValidationError(
                {
                    "supplier_delivers": ValidationError(
                        _("only one can deliver, please remove one of these options")
                    ),
                    "driver": ValidationError(_("only one can deliver, please remove one of these options")),
                }
            )

    def save(self, *args, **kwargs):
        order = self.order
        if self.loads > order.nloads():
            return ValidationError({"loads": "more loads scheudled than the amount ordered"})
        if self.loads > 0:
            order.dloads += self.loads
            order.save()
            order.refresh_from_db()
        if order.nloads() == 0 and self.ddate is not None:
            self.status = StatusChoices.COMPLETE
        elif order.rloads > order.nloads() > 0:
            self.status = StatusChoices.IN_PROGRESS

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

    Args:
        supplier_delivers   (bool):         BooleanField
        driver              (int):          ForeignKey  -> User
        crew                (str):          CharField
        pdate               (date):         DateField
        ctime               (datetime):     DateTimeField
        loads               (float):        FloatField
        progress            (str):          CharField
    """
    supplier_delivers = models.BooleanField(
        _("supplier delivers"),
        default=False,
        help_text="Check if the supplier is responsible for delivering the order",
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("delivery driver"),
        related_name="pump_schedules",
        limit_choices_to={"groups__name": "Drivers"},
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    crew = models.CharField(_("crew pouring"), max_length=150, blank=True, null=True)
    pdate = models.DateField(_("pour date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    ctime = models.TimeField(_("concrete time"), auto_now=False, auto_now_add=False, blank=True, null=True)
    loads = models.FloatField(_("loads"), default=0)
    progress = models.CharField(
        _("pump progress"), choices=PourProgress.choices, default=PourProgress.WILL_CALL, max_length=11
    )
    order = models.ForeignKey(
        ConcreteOrder,
        verbose_name=_("concrete order"),
        related_name="pump_schedule",
        on_delete=models.CASCADE,
    )
    history = HR()

    @admin.display(description="Driver")
    def get_driver(self):
        """if supplier_delivers return supplier name, otherwise return the driver's full name"""

        if self.supplier_delivers:
            order = ConcreteOrder.objects.get(pk=self.order.pk)
            return "{0}".format(order.supplier)
        return "{0}".format(self.driver.get_full_name())

    def clean(self):
        """
        Require at least one of supplier_delivers or driver to be set - but not both
        """
        if not (self.supplier_delivers or self.driver):
            raise ValidationError(
                {
                    "supplier_delivers": ValidationError(_("Someone must deliver the order.")),
                    "driver": ValidationError(_("Someone must deliver the order.")),
                }
            )
        if (self.supplier_delivers and self.driver):
            raise ValidationError(
                {
                    "supplier_delivers": ValidationError(
                        _("only one can deliver, please remove one of these options")
                    ),
                    "driver": ValidationError(_("only one can deliver, please remove one of these options")),
                }
            )

    def __str__(self) -> str:
        """label for class instance

        Returns:
            str: first letter of first name, full last name, instance pk
        """
        return "{0} [{1}]".format(self.get_driver(), self.order.po)

    class Meta:
        db_table = "concrete_pump_schedule"
        managed = True
        verbose_name = "concrete pump schedule"
