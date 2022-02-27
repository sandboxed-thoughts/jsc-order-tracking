from django.db import models
from django.forms import ChoiceField
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords as HR

class GravelOrder(models.Model):
    """Gravel order log for tracking and managing gravel orders
    """
    
    bldr = models.CharField(_("Builder"), max_length=50)
    job_site = models.CharField(_("Job Site"), max_length=50)
    lot = models.PositiveSmallIntegerField(_("Lot Number"))
    caller = models.CharField(_("Caller"), max_length=50)
    r_loads = models.PositiveIntegerField(_("Loads Requested"))
    d_loads = models.PositiveIntegerField(_("Loads Delivered"), blank=True, null=True)
    stone = models.CharField(_("Stone Type"), max_length=50)
    bsdt = models.CharField(_("B/S D/T"), max_length=50)
    supplier = models.CharField(_("Supplier"), max_length=50)
    driver = models.CharField(_("Driver"), max_length=50, blank=True, null=True)
    n_date = models.DateField(_("Date Needed"), auto_now=False, auto_now_add=False)
    d_date = models.DateField(_("Date Delivered"), auto_now=False, auto_now_add=False, blank=True, null=True)
    priority = models.CharField(_("Priority"), max_length=50)
    po = models.PositiveIntegerField(_("P.O. Number"))
    history = HR()
    
    def __str__(self) -> str:
        return "{0} [{1}] {2}".format(self.job_site,self.lot,self.pk)

    class Meta:
        db_table = 'g_orders'
        managed = True
        verbose_name = 'Gravel Order'
        verbose_name_plural = 'Gravel Orders'