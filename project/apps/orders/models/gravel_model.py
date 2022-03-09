from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import BaseOrder
from simple_history.models import HistoricalRecords as HR
from django.utils.html import format_html as fh


class Gravel(BaseOrder):
    """Gravel order log for tracking and managing gravel orders
    
    Fields:
        caller:         models.CharField(_("Caller"), max_length=50)
        bsdt:           models.CharField(_("B/S D/T"), max_length=3, choices=BSDT.choices, default=BSDT.B)
        priority:       models.CharField(_("Priority"), max_length=50)
        rloads:         models.PositiveIntegerField(_("Loads Requested"),)
        dloads:         models.PositiveIntegerField(_("Loads Delivered"),)
        ndate:          models.DateField(_("Date Needed"), auto_now=False, auto_now_add=False, blank=True, null=True)
        ddate:          models.DateField(_("Delivery / Pour Date"), auto_now=False, auto_now_add=False, blank=True, null=True)
        supplier:       models.ForeignKey("suppliers.Supplier", verbose_name="supplier", related_name="gravel_orders", on_delete=models.CASCADE)
        stype:          models.ForeignKey("suppliers.StoneType", verbose_name="stone type", related_name="orders", on_delete=models.CASCADE)
        driver:         models.CharField(_("Driver"), max_length=25, blank=True, null=True)
        is_complete:    models.BooleanField(_("Order Complete"), default=False)
        history:        HR(inherit=True)

    """

    # choices
    class BSDT:
        B = "B/S"
        D = "D/T"
        choices = [
            (B, "B/S"),
            (D, "D/T"),
        ]

    # fields
    job_site = models.ForeignKey(
        "jobs.JobSite", verbose_name=_("Job Site"), related_name="gravel_orders", on_delete=models.CASCADE
    )
    caller = models.CharField(_("Caller"), max_length=50)
    bsdt = models.CharField(_("B/S D/T"), max_length=3, choices=BSDT.choices, default=BSDT.B)
    priority = models.CharField(_("Priority"), max_length=50)
    rloads = models.PositiveIntegerField(_("Loads Requested"),)
    dloads = models.PositiveIntegerField(_("Loads Delivered"),)
    ndate = models.DateField(_("Date Needed"), auto_now=False, auto_now_add=False, blank=True, null=True)
    ddate = models.DateField(_("Delivery / Pour Date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    supplier = models.ForeignKey("suppliers.Supplier", verbose_name="supplier", related_name="gravel_orders", on_delete=models.PROTECT)
    stype = models.ForeignKey("suppliers.StoneType", verbose_name="stone type", related_name="orders", on_delete=models.PROTECT)
    driver = models.CharField(_("Driver"), max_length=25, blank=True, null=True)
    is_complete = models.BooleanField(_("Order Complete"), default=False)
    history = HR(inherit=True)

    def __str__(self) -> str:
        return "Order: {0} - Site: {1}".format(self.po, self.job_site)

    
        

    def save(self, *args, **kwargs):
        if self.rloads == self.dloads:
            self.is_complete=True
        super(Gravel, self).save(*args, **kwargs)

    class Meta:
        db_table = "g_orders"
        managed = True
        verbose_name = "Gravel Order"
        verbose_name_plural = "Gravel Orders"
