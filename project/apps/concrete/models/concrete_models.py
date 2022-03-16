from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.concrete.helpers import MixChoices
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
        temp (str):         CharField
        precip (str):       CharField

    """

    po = models.CharField(_("purchase order"), max_length=50, validators=[RegexValidator("[\\S\\w]")])
    lots = models.ManyToManyField("clients.Lot", verbose_name=_("lots"), related_name="orders")
    supplier = models.ForeignKey("suppliers.Supplier", verbose_name=_("supplier"), on_delete=models.PROTECT)
    dispatcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("dispatcher"),
        related_name="corders_accepted",
        on_delete=models.PROTECT,
    )
    etotal = models.SmallIntegerField(
        _("estimated total"),
    )
    atotal = models.SmallIntegerField(_("actual total"), blank=True, null=True)
    qordered = models.SmallIntegerField(
        _("total ordered"),
    )
    mix = models.CharField(_("mix"), max_length=10, choices=MixChoices.choices, default=MixChoices.STANDARD)
    slump = models.CharField(_("slump"), max_length=6)

    def __str__(self) -> str:
        return "{0} [{1}] for {2}".format(self.po, "/".join(self.mix, self.slump))

    class Meta:
        db_table = "orders_concrete"
        managed = True
        verbose_name = "Concrete Order"
        verbose_name_plural = "Concrete Orders"


class FootingsOrder(ConcreteOrder):
    """Extends the Concrete Order model

    fields:
        garage (str):   CharField
        wea (str):      CharField
        history (int):  ForeignKey -> HistoryRecord
    """

    class GarageChoices:
        FT4 = "4'"
        FT8 = "8'"
        FT9 = "9'"

        choices = [
            (FT4, "4'"),
            (FT8, "8'"),
            (FT9, "9'"),
        ]

    garage = models.CharField(_("garage size"), choices=GarageChoices.choices, default=GarageChoices.FT8, max_length=3)
    wea = models.CharField(_("walkout egress area"), max_length=50)
    history = HR(inherit=True)

    def __str__(self) -> str:
        return "footings order - " + super().__str__()

    class Meta:
        db_table = "orders_concrete_footings"
        managed = True
        verbose_name = "flatwork order"


class FlatworkItem(models.Model):
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("item description"))


class FlatworkOrder(ConcreteOrder):
    items = models.ManyToManyField("FlatworkItem", verbose_name=_("items"), through="FlatworkOrderItems")
    history = HR(inherit=True)

    def __str__(self) -> str:
        return "flatwork order - " + super().__str__()

    class Meta:
        db_table = "orders_concrete_flatwork"
        managed = True
        verbose_name = "Wall Order"
        verbose_name_plural = "Wall Orders"


class WallOrder(ConcreteOrder):
    """Extends the Concrete order model

    fields:
        history (int):  ForeignKey -> HistoryRecord
    """

    history = HR(inherit=True)

    def __str__(self) -> str:
        return "wall order - " + super().__str__()

    class Meta:
        db_table = "orders_concrete_walls"
        managed = True
        verbose_name = "Wall Order"
        verbose_name_plural = "Wall Orders"
