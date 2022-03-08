from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import BaseOrder
from simple_history.models import HistoricalRecords as HR


class Gravel(BaseOrder):
    """Gravel order log for tracking and managing gravel orders"""

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
    history = HR(inherit=True)

    def __str__(self) -> str:
        return "{0} [{1}] {2}".format(self.job_site, self.lot, self.pk)

    class Meta:
        db_table = "g_orders"
        managed = True
        verbose_name = "Gravel Order"
        verbose_name_plural = "Gravel Orders"
