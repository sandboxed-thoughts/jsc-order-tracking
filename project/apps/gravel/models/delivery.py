from lib2to3.pgen2 import driver
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords as HR
from django.conf import settings
from .gravel_orders import GravelOrder
from django.utils import timezone

class GravelDelivery(models.Model):

    class StatusChoices:
        SCHEDULED = 'scheduled'
        IN_PROGRESS = 'in progress'
        COMPLETE = 'complete'

        choices = [
            (SCHEDULED, 'scheduled'),
            (IN_PROGRESS, 'in progress'),
            (COMPLETE, 'complete'),
        ]


    order = models.ForeignKey(GravelOrder, verbose_name=_("order"), on_delete=models.PROTECT)
    ddriver = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("delivery driver"), related_name="deliveries",on_delete=models.PROTECT)
    sdate = models.DateField(_("scheduled for"), auto_now=False, auto_now_add=False, default=timezone.now)
    loads = models.SmallIntegerField(_("loads"), default=1)
    notes = models.TextField(_("notes"), blank=True, null=True)
    status = models.CharField(_("status"), max_length=11, choices=StatusChoices.choices, default=StatusChoices.SCHEDULED)
    history = HR()

    def __str__(self) -> str:
        return "{0}. {1} [{2}]".format(self.ddriver.first_name[0].capitalize(), self.ddriver.last_name.title(), self.pk)

    def save(self, *args, **kwargs):

        super(GravelDelivery, self).save(*args, **kwargs) # Call the real save() method

    class Meta:
        db_table = 'orders_gravel_deliveries'
        managed = True
        verbose_name = 'Gravel Delivery'
        verbose_name_plural = 'Gravel Deliveries'