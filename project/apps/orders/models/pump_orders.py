from typing import Iterable, Optional

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.clients.models import Site
from apps.core.admin import get_notes
from apps.core.models import NoteModel
from simple_history.models import HistoricalRecords as HR

from ..helpers import get_po


class PumpOrder(models.Model):
    """Django model for pump rentals

    Args:
        po (int):
        pump_supplier (int):    ForeignKey -> Supplier
        builder (int):          ForeignKey -> Builder
    """

    # pump info
    id = models.BigAutoField(_("purchase order"), primary_key=True, unique=True, blank=False, null=False)
    po = models.BigIntegerField(_("PO"), unique=True, primary_key=False)
    pump_supplier = models.ForeignKey(
        "supplies.Supplier",
        verbose_name=_("pump supplier"),
        related_name="pump_orders",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    builder = models.ForeignKey(
        "clients.Client", verbose_name=_("builder"), related_name="pump_orders", on_delete=models.CASCADE
    )
    site = models.ForeignKey("clients.Site", verbose_name=_("Subdivision"), on_delete=models.CASCADE)
    description = models.TextField(
        _("additional info"),
        blank=True,
        null=True,
    )
    created_on = models.DateTimeField(_("created on"), auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True, auto_now_add=False)
    history = HR()

    objects = models.Manager()

    def __str__(self) -> str:
        return "{0}".format(str(self.po).zfill(6))

    @admin.display(description="", empty_value="")
    def get_notes(self):
        return get_notes(self.pump_order_notes.all().order_by("created_on"))

    @admin.display(description="concrete order", empty_value="N/A")
    def concrete(self):
        return self.concrete_order or None

    def save(self, *args, **kwargs):
        if not self.po:
            self.po = get_po()
        super(PumpOrder, self).save()

    class Meta:
        db_table = "orders_concrete_pumps"
        managed = True
        verbose_name = "pump rental"
        verbose_name_plural = "pump rentals"


class PumpOrderNote(NoteModel):
    order = models.ForeignKey(
        PumpOrder,
        verbose_name=_("pump order"),
        related_name="pump_order_notes",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "orders_pump_order_notes"
        managed = True
        verbose_name = "order note"
        verbose_name_plural = "order notes"
