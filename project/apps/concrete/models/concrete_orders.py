from random import choices
from django.db import models
from django.contrib import admin
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords as HR

class ConcreteOrder(models.Model):
    """Django model for concrete orders
    
    fields:
        po (str):           CharField
        lots (int):         ForeignKey
        supplier (int):     ForeignKey
        dispatcher ():      ForeignKey
        etotal (int):       SmallIntegerField
        atotal (int):       SmallIntegerField
        qordered (int):     SmallIntegerField
        mix (str):          CharField
        slump (str):        CharField
        is_pump (bool):     BooleanField
        pinfo (str):        TextField
        temp (str):         CharField
        precip (str):       CharField

    """

    class MixChoices:
        RICH = 'rich'
        STANDARD = 'standard'
        MEDIUM = 'medium'
        LEAN = 'lean'

        choices = [
            (RICH, 'rich'),
            (STANDARD, 'standard'),
            (MEDIUM, 'medium'),
            (LEAN, 'lean'),
        ]

    class TempChoices:
        NONE = None
        HIGH = 'high'
        LOW = 'low'

        choices = [
            (NONE, None),
            (HIGH, 'high'),
            (LOW, 'low'),
        ]

    class PrecipChoices:
        CLEAR = None
        RAIN = 'rain'
        SNOW = 'snow'

        choices = [
            (CLEAR, None),
            (RAIN, 'rain'),
            (SNOW, 'snow'),
        ]

    po = models.CharField(_("Purchase Order"), max_length=50, validators=[RegexValidator("[\\S\\w]")])
    lots = models.ManyToManyField("clients.Lot", verbose_name=_("lots"), related_name='orders')
    supplier = models.ForeignKey("suppliers.Supplier", verbose_name=_("supplier"), on_delete=models.PROTECT)
    dispatcher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("dispatcher"), related_name='corders_accepted', on_delete=models.PROTECT)
    etotal = models.SmallIntegerField(_("estimated total"),)
    atotal = models.SmallIntegerField(_("actual total"), blank=True, null=True)
    qordered = models.SmallIntegerField(_("total ordered"),)
    mix = models.CharField(_("mix"), max_length=10, choices=MixChoices.choices, default=MixChoices.STANDARD)
    slump = models.CharField(_("slump"), max_length=6)
    is_pump = models.BooleanField(_("pump"),default=True)
    pinfo = models.TextField(_("pump info"), blank=True, null=True)
    temp = models.CharField(_("temperature"), max_length=4, blank=True, null=True, choices=TempChoices.choices, default=TempChoices.NONE)
    precip = models.CharField(_("inclimate weather"), max_length=5, blank=True, null=True, choices=PrecipChoices.choices, default=PrecipChoices.CLEAR)
    history = HR(inherit=True)

    def __str__(self) -> str:
        return "{0} [{1}] for {2}".format(self.po, "/".join(self.mix,self.slump))

        

    class Meta:
        db_table = 'orders_concrete'
        managed = True
        verbose_name = 'Concrete Order'
        verbose_name_plural = 'Concrete Orders'



class WallOrder(ConcreteOrder):
    pass

class FootingsOrder(ConcreteOrder):
    """Extends the Concrete Order model"""

    class GarageChoices:
        FT4 = "4'"
        FT8 = "8'"
        FT9 = "9'"

        choices = [
            (FT4, "4'"),
            (FT8, "8'"),
            (FT9, "9'"),
        ]
    
    garage = models.CharField(_("garage"), max_length=4, choices=GarageChoices.choices,default=GarageChoices.FT8)
    wea = models.CharField(_("walkout egress area"), max_length=50)
    history = HR(inherit=True)

    class Meta:
        db_table = 'orders_concrete_wall'
        managed = True
        verbose_name = "Footings Order"
        verbose_name_plural = "Footings Orders"