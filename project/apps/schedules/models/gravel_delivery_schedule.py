from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.admin import get_notes
from apps.orders.models import GravelOrder
from simple_history.models import HistoricalRecords as HR

from ..helpers import StatusChoices

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

    @admin.display(description="delivery driver", ordering="driver")
    def get_driver(self):
        """if supplier_delivers return supplier name, otherwise return the driver's full name"""

        if self.supplier_delivers:
            return self.order.supplier.name
        return self.driver.get_full_name()

    @admin.display(description="item", ordering="order__item")
    def order_item(self):
        if self.order.item:
            return self.order.item
        return "None"

    @admin.display(description="builder", ordering="order__builder")
    def order_builder(self):
        if self.order.builder:
            return self.order.builder.name.title()
        return "None"

    @admin.display(description="supplier", ordering="order__supplier")
    def order_supplier(self):
        if self.order.supplier:
            return self.order.supplier.name.title()
        return "None"

    @admin.display(description="lots", ordering="order__lots")
    def order_lots(self):
        if self.order.lots:
            return self.order.get_lots()
        return "None"

    @admin.display(description="", empty_value="")
    def get_notes(self):
        return get_notes(self.gravel_delivery_notes.all())

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
            return ValidationError({"loads": "more loads scheduled than the amount ordered"})
        if (self.status == StatusChoices.COMPLETE) and (self.loads > 0):
            order.dloads += self.loads
            order.save()
            order.refresh_from_db()
        super(GravelDeliverySchedule, self).save(*args, **kwargs)  # Call the real save() method

    class Meta:
        db_table = "orders_gravel_deliveries"
        managed = True
        verbose_name = "Gravel Delivery"
        verbose_name_plural = "Gravel Deliveries"
        ordering = ["-sdate", "driver"]
