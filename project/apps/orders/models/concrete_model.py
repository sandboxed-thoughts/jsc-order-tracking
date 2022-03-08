from random import choices
from django.db import models
from django.utils.html import format_html as fh
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords as HR
from .base import BaseOrder


class Concrete(BaseOrder):

    """
    Concrete order tracking model.
    """

    # choices
    class OrderType:
        WALLS = "walls"
        FLATWORK = "flatwork"
        FOOTINGS = "footings"

        choices = [
            (FLATWORK, "flatwork"),
            (FOOTINGS, "footings"),
            (WALLS, "walls"),
        ]

    class ConcreteType:
        MIX = "mix"
        SLUMP = "slump"

        choices = [
            (MIX, "mix"),
            (SLUMP, "slump"),
        ]

    # fields
    job_site = models.ForeignKey(
        "jobs.JobSite", verbose_name=_("Job Site"), related_name="concrete_orders", on_delete=models.CASCADE
    )
    otype = models.CharField(_("Pour Type"), max_length=8, choices=OrderType.choices)
    dsph = models.CharField(_("Dispatcher"), max_length=50)
    ctype = models.CharField(_("Mix/Slump"), max_length=5, choices=ConcreteType.choices)
    pump = models.BooleanField(_("Pump"), default=False)
    pinfo = models.TextField(_("Pump Info"), max_length=150, blank=True, null=True)
    iagt = models.CharField(_("Inspection Agency"), max_length=50, blank=True, null=True)
    itime = models.DateTimeField(_("Inspection Time"), auto_now=False, auto_now_add=False, blank=True, null=True)
    garage = models.PositiveSmallIntegerField(
        _("Garage Height (ft)"), blank=True, null=True, help_text="only for footings"
    )
    wea = models.PositiveSmallIntegerField(
        _("Walkout Egress Area (ft)"), blank=True, null=True, help_text="only for footings"
    )
    history = HR(inherit=True)

    def __str__(self) -> str:
        return "{0} [order: {1}] {2}".format(self.job_site, self.po, self.pk)

    class Meta:
        db_table = "c_orders"
        managed = True
        verbose_name = "Concrete Order"
        verbose_name_plural = "Concrete Orders"
