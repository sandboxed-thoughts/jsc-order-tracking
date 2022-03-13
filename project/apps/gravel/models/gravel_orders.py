from django.db import models
from django.contrib import admin
from django.core.validators import RegexValidator

from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords as HR

class GravelOrder(models.Model):
    """Django model for gravel orders
    
    Fields:
        po (str): CharField
        priority (str): CharField
        lot (int): ForeignKey
        item (int): ForeignKey
        bsdt (str): CharField
        supplier (int): ForeignKey
        need_by (datetime): DateField
        rloads (int): SmallIntegerField
        dloads (int): SmallIntegerField
        ddate (datetime): DateField
        history (class): HistoricalRecords 

    methods:     
        nloads (int): returns the remaining loads to complete the order
        is_complete (bool): status
    """

    po = models.CharField(_("Purchase Order"), max_length=50, validators=[RegexValidator("[\\S\\w]")])
    priority = models.CharField(_("priority"), max_length=50)
    lot = models.ForeignKey("clients.Lot", verbose_name=_("lot"), on_delete=models.PROTECT)
    item = models.ForeignKey("suppliers.StoneType", verbose_name=_("stone type"), on_delete=models.PROTECT)
    bsdt = models.CharField(_("B/S D/T"), max_length=50,blank=True, null=True)
    supplier = models.ForeignKey("suppliers.Supplier", verbose_name=_("supplier"), on_delete=models.PROTECT)
    need_by = models.DateField(_("date needed"), auto_now=False, auto_now_add=False)
    rloads = models.SmallIntegerField(_("loads requested"))
    dloads = models.SmallIntegerField(_("loads delivered"), default=0)
    ddate = models.DateField(_("date delivered"), auto_now=False, auto_now_add=False, blank=True, null=True)
    history = HR()

    class Meta:
        db_table = 'orders_gravel'
        managed = True
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


    def __str__(self) -> str:
        return "{0} [{1}] for {2}".format(self.item, self.po, self.lot)

    @admin.display(description='loads needed')
    def nloads(self) -> int:
        return self.rloads - self.dloads

    def is_complete(self) -> bool:
        if (self.nloads <= 0):
            return True
