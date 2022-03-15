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
        is_pump (bool):     BooleanField
        pinfo (str):        TextField
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
    onotes = models.TextField(_("Order Notes"), blank=True, null=True)
    history = HR(inherit=True)

    def __str__(self) -> str:
        return "{0} [{1}] for {2}".format(self.po, "/".join(self.mix, self.slump))

    def is_pump(self) -> bool:
        if self.pinfo is not None:
            return True
        return False

    class Meta:
        db_table = "orders_concrete"
        managed = True
        verbose_name = "Concrete Order"
        verbose_name_plural = "Concrete Orders"


class WallOrder(models.Model):
    order = models.OneToOneField(ConcreteOrder, verbose_name=_("order"), on_delete=models.CASCADE, primary_key=True)
    history = HR(inherit=True)

    class Meta:
        db_table = "orders_concrete_walls"
        managed = True
        verbose_name = "Wall Order"
        verbose_name_plural = "Wall Orders"


class FootingsOrder(models.Model):
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

    order = models.OneToOneField(ConcreteOrder, verbose_name=_("order"), on_delete=models.CASCADE, primary_key=True)
    garage = models.CharField(_("garage"), max_length=4, choices=GarageChoices.choices, default=GarageChoices.FT8)
    wea = models.CharField(_("walkout egress area"), max_length=50)
    history = HR(inherit=True)

    class Meta:
        db_table = "orders_concrete_footings"
        managed = True
        verbose_name = "Footings Order"
        verbose_name_plural = "Footings Orders"


class FlatworkOrder(models.Model):
    order = models.OneToOneField(ConcreteOrder, verbose_name=_("order"), on_delete=models.CASCADE, primary_key=True)
    items = models.ManyToManyField(
        "suppliers.ConcreteItems",
        verbose_name=_("Items"),
        related_name="concrete_orders",
    )

    history = HR(inherit=True)

    class Meta:
        db_table = "orders_concrete_flatwork"
        managed = True
        verbose_name = "Flatwork Order"
        verbose_name_plural = "Flatwork Orders"
