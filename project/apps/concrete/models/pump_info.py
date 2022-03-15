from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords as HR
from ..models import ConcreteOrder
from ..helpers import PourProgress, PrecipDelay, TempDelay


class PumpInfo(models.Model):
    """Model for storing pump schedule and details
    
    fields:         
        crew (str):             CharField
        ctime (datetime):       DateTimeField
        temp (str):             CharField
        precip (str):           CharField
        progress (str):         CharField

    returns (str):
        "{0} {1}".format(self.crew, self.ctime)
    """
    order = models.OneToOneField(ConcreteOrder, on_delete=models.CASCADE,blank=True, null=True)
    crew = models.CharField(_("crew pouring"), max_length=50, blank=True, null=True)
    ctime = models.DateTimeField(_("concrete time"), auto_now=False, auto_now_add=False, blank=True, null=True)
    temp = models.CharField(
        _("temperature"), max_length=4, blank=True, null=True, choices=TempDelay.choices, default=TempDelay.NONE
    )
    precip = models.CharField(
        _("inclimate weather"),
        max_length=5,
        blank=True,
        null=True,
        choices=PrecipDelay.choices,
        default=PrecipDelay.CLEAR,
    )
    progress = models.CharField(_("pour progress"), max_length=15, choices=PourProgress.choices)
    pnotes = models.TextField(_("Order Notes"), blank=True, null=True)

    def __str__(self):
        return "{0} {1}".format(self.crew, self.ctime)

    class Meta:
        db_table = "orders_concrete_pumpinfo"
        managed = True
        verbose_name = "Pump Info"
