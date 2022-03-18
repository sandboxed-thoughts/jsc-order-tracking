from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.concrete.helpers import GarageChoices
from apps.core.models import NoteModel
from simple_history.models import HistoricalRecords as HR
from ..managers import (WallManager, FootingsManager, FlatworkManager)


class ConcreteOrder(models.Model):
    """Django model for concrete orders

    fields:
        po (str):           CharField
        lots (int):         ForeignKey -> Lot
        supplier (int):     ForeignKey -> Supplier
        dispatcher ():      ForeignKey -> AUTH_USER_MODEL
        etotal (int):       SmallIntegerField
        atotal (int):       SmallIntegerField
        qordered (int):     SmallIntegerField
        temp (str):         CharField
        precip (str):       CharField
        items (int):        ForeignKey -> FlatworkItem
        garage (char):      CharField
        wea (char):         CharField

    """

    is_wall = models.BooleanField(_("is wall order"), default=True)
    is_footings = models.BooleanField(_("is footing order"), default=False)
    is_flatwork = models.BooleanField(_("is flatwork order"), default=False)
    po = models.CharField(_("purchase order"), max_length=50, validators=[RegexValidator("[\\S\\w]")], unique=True)
    lots = models.ManyToManyField("clients.Lot", verbose_name=_("lots"), through="ConcreteOrderLot")
    ctype = models.ForeignKey("suppliers.ConcreteType", verbose_name=_("concrete type"), on_delete=models.PROTECT)
    supplier = models.ForeignKey("suppliers.Supplier", verbose_name=_("supplier"), related_name="supplier_concrete_orders", on_delete=models.PROTECT)
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
    # flatwork order parts
    items = models.ManyToManyField("FlatworkItem", verbose_name=_("flatwork items"), through="FlatworkOrderItems")
    # footings order parts
    garage = models.CharField(
        _("garage size"),
        choices=GarageChoices.choices,
        default=GarageChoices.NONE,
        max_length=3,
        blank=True,
        null=True,
    )
    wea = models.CharField(_("walkout egress area"), max_length=50, blank=True, null=True)
    order_date = models.DateTimeField(_("order date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    history = HR()

    def __str__(self) -> str:
        return "{0} [{1}]".format(self.supplier, self.po)

    objects = models.Manager()
    wall_orders = WallManager()
    footings_orders = FootingsManager()
    flatwork_orders = FlatworkManager()

    class Meta:
        db_table = "orders_concrete"
        managed = True
        verbose_name = "concrete order"
        verbose_name_plural = "concrete orders"


class FlatworkOrder(ConcreteOrder):
    class Meta:
        proxy = True
        verbose_name = "flatwork order"

    objects = FlatworkManager()

    def save(self, *args, **kwargs):
        self.is_wall = False
        self.is_footings = False
        self.is_flatwork = True
        super().save(*args, **kwargs)  # Call the "real" save() method.


class WallOrder(ConcreteOrder):
    class Meta:
        proxy = True
        verbose_name = "wall order"

    objects = WallManager()

    def save(self, *args, **kwargs):
        self.is_wall = True
        self.is_footings = False
        self.is_flatwork = False
        super().save(*args, **kwargs)  # Call the "real" save() method.


class FootingsOrder(ConcreteOrder):
    class Meta:
        proxy = True
        verbose_name = "footings order"

    objects = FootingsManager()

    def save(self, *args, **kwargs):
        self.is_wall = False
        self.is_footings = True
        self.is_flatwork = False
        super().save(*args, **kwargs)  # Call the "real" save() method.


class FlatworkItem(models.Model):
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("item description"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "orders_concrete_flatwork_items"
        managed = True
        verbose_name = "flatwork item"
        verbose_name_plural = "flatwork items"


class ConcreteOrderNote(NoteModel):
    order = models.ForeignKey("ConcreteOrder", verbose_name=_("concrete order notes"), related_name="concrete_order_notes", on_delete=models.CASCADE)

    class Meta:
        db_table = "orders_concrete_notes"
        managed = True
        verbose_name = "order note"
        verbose_name_plural = "order notes"
