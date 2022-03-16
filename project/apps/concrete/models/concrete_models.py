from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import NoteModel
from apps.concrete.helpers import MixChoices, GarageChoices
from simple_history.models import HistoricalRecords as HR


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
        mix (str):          CharField
        slump (str):        CharField
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
    # flatwork order parts
    items = models.ManyToManyField("FlatworkItem", verbose_name=_("items"), through="FlatworkOrderItems")
    # footings order parts
    garage = models.CharField(_("garage size"), choices=GarageChoices.choices, default=GarageChoices.NONE, max_length=3, blank=True, null=True)
    wea = models.CharField(_("walkout egress area"), max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return "{0} [{1}] for {2}".format(self.supplier, self.po, "/".join(self.mix, self.slump))

    class Meta:
        db_table = "concrete_orders"
        managed = True
        verbose_name = "concrete orders"


class FlatworkItem(models.Model):
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("item description"))

    class Meta:
        db_table = "orders_concrete_flatwork_items"


class OrderNotes(NoteModel):
    order = models.ForeignKey("ConcreteOrder", verbose_name=_("concrete order notes"), on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders_concrete_notes'
        managed = True
        verbose_name = "order note"
        verbose_name_plural = "order notes"
