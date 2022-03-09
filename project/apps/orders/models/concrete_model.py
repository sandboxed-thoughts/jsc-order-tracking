from django.db import models
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords as HR

from .base import BaseOrder


class Concrete(BaseOrder):
    """A Django model for Concrete Orders

    Fields:
        job_site (int): the pk of the JobSite for delivery
        otype (str): A choice of order types based on placement of the material
        ctype (int): The pk of the StoneType ordered
        dsph (str): The the supplier contact responsible for accepting the order
        ptype (str): A choice of Mix or Slump
        pump (bool): True if the order requires pumping
        pinfo (str): A string of information about the pump process
        iagt (str):  The Inspection agency responsible for certifying the job
        itime (datetime): The scheduled appointment for an Inspection
        garage (int): The height of the garage
        wea (int): The Walkout Egress Area
        qord (int): Quantity Orderd
        qtype (char): Units of measurement for the quantity ordered
        etot (int): Estimated total quantity of units ordered
        atot (int): Actual total quantity of units ordered
        crew (str): The people delivering or pouring
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

    class QTypeChoices:
        CUYD = "cu yd"
        SQFT = "sqft"
        LBS = "lbs"
        BAGS = "bags"

        choices = [
            (
                "Large Loads",
                (
                    (CUYD, "cu yd"),
                    (SQFT, "sqft"),
                ),
            ),
            (
                "Regular Loads",
                (
                    (LBS, "lbs"),
                    (BAGS, "bags"),
                ),
            ),
        ]

    class PourType:
        MIX = "mix"
        SLUMP = "slump"

        choices = [
            (MIX, "mix"),
            (SLUMP, "slump"),
        ]

    # fields
    job_site = models.ForeignKey(
        "jobs.JobSite", verbose_name=_("Subdivision"), related_name="concrete_orders", on_delete=models.CASCADE
    )
    otype = models.CharField(_("Pour Type"), max_length=8, choices=OrderType.choices)
    supplier = models.ForeignKey(
        "suppliers.Supplier", verbose_name="supplier", related_name="concrete_orders", on_delete=models.PROTECT
    )

    ctype = models.ForeignKey(
        "suppliers.ConcreteType", verbose_name=_("Concrete Type"), related_name="orders", on_delete=models.CASCADE
    )
    dsph = models.CharField(_("Dispatcher"), max_length=50)
    ptype = models.CharField(_("Mix/Slump"), max_length=5, choices=PourType.choices)
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
    qord = models.PositiveIntegerField(_("Quantity Ordered"), default=0)
    qtype = models.CharField(_("Quantity Type"), max_length=5, choices=QTypeChoices.choices, default=QTypeChoices.SQFT)
    etot = models.PositiveIntegerField(_("Estimated Total"), help_text="leave blank if same as quantity ordered")
    atot = models.PositiveIntegerField(_("Actual Total"), default=0)
    crew = models.CharField(_("Delivery / Pour Crew"), max_length=50, blank=True, null=True)

    history = HR(inherit=True)

    def __str__(self) -> str:
        return "{0} [order: {1}] {2}".format(self.job_site, self.po, self.pk)

    def save(self, *args, **kwargs):
        if not self.etot:
            self.etot = self.qord
        if self.rloads == self.dloads:
            self.is_complete = True
        if self.progress == "complete":
            self.is_complete = True
        super(Gravel, self).save(*args, **kwargs)

    class Meta:
        db_table = "c_orders"
        managed = True
        verbose_name = "Concrete Order"
        verbose_name_plural = "Concrete Orders"
