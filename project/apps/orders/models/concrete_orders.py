from django.conf import settings
from django.contrib import admin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.html import format_html as fh
from django.utils.translation import gettext_lazy as _

from apps.core.helpers import get_lots
from apps.core.models import NoteModel
from simple_history.models import HistoricalRecords as HR

from ..helpers import GarageChoices
from .inspection_models import InspectionModel


class FlatworkItem(models.Model):
    order = models.ForeignKey("ConcreteOrder", verbose_name=_("order"), on_delete=models.CASCADE)
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

    order = models.ForeignKey(
        "ConcreteOrder", verbose_name=_("concrete order"), related_name="concrete_orders", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "orders_concrete_order_notes"
        managed = True
        verbose_name = "order note"
        verbose_name_plural = "order notes"


class ConcreteOrder(models.Model):
    """Django model for concrete orders

    Args:
        builder (int):          ForeignKey -> Builder
        site (int):             ForeignKey -> SiteModel
        lots (str):             CharField
        cinfo (int):            ForeignKey -> ConcreteType
        etotal (int):           SmallIntegerField
        atotal (int):           SmallIntegerField
        qordered (int):         SmallIntegerField
        fitems (int):           ForeignKey -> FlatworkItem
        po (str):               CharField
        date_needed (time):     DateTimeField
        date_created (time):    DateTimeField
        order_notes (str):      TextField
        supplier (int):         ForeignKey -> Supplier
        dispatcher ():          ForeignKey -> AUTH_USER_MODEL
        temp (str):             CharField
        precip (str):           CharField

    """

    # client info
    builder = models.ForeignKey(
        "clients.BuilderModel",
        verbose_name=_("builder"),
        related_name="builder_concrete_orders",
        on_delete=models.CASCADE,
    )
    site = models.ForeignKey(
        "sites.SiteModel", verbose_name=_("site"), related_name="site_concrete_orders", on_delete=models.CASCADE
    )
    lots = models.CharField(
        _("lots"), max_length=150, help_text='separate each lot with a comma, ex "15446, 4789, 14,2546"'
    )
    etotal = models.SmallIntegerField(
        _("estimated total"),
    )
    atotal = models.SmallIntegerField(_("actual total"), blank=True, null=True)
    qordered = models.SmallIntegerField(
        _("total ordered"),
    )
    # order info
    po = models.CharField(_("purchase order"), max_length=50, validators=[RegexValidator("[\\S\\w]")], unique=True)
    date_needed = models.DateField(_("date needed"), auto_now=False, auto_now_add=False, blank=True, null=True)
    date_created = models.DateTimeField(_("created on"), auto_now=False, auto_now_add=True)
    order_notes = models.ManyToManyField("core.NoteModel", verbose_name=_("notes"), through=ConcreteOrderNote)
    supplier = models.ForeignKey(
        "suppliers.Supplier",
        verbose_name=_("supplier"),
        related_name="supplier_concrete_orders",
        on_delete=models.PROTECT,
    )
    dispatcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("dispatcher"),
        related_name="corders_accepted",
        limit_choices_to={"groups__name": "Dispatchers"},
        on_delete=models.PROTECT,
    )
    inspection = models.ForeignKey(
        InspectionModel, verbose_name=_("inspection"), on_delete=models.CASCADE, blank=True, null=True
    )
    # history
    history = HR()

    def __str__(self) -> str:
        return "{0} [{1}]".format(self.builder, self.po)

    objects = models.Manager()

    @admin.display(description="lots")
    def get_lots(self):
        return get_lots(self.lots)

    @admin.display(description="notes")
    def get_notes(self):
        nl = ['{0}:<br>&ensp;"{1}"'.format(x.author, x.note) for x in self.order_notes.all()]
        pnl = "<br>".join(nl)
        return fh(pnl)

    @admin.display(description="concrete")
    def get_ctypes(self):
        cl = [x.__str__() for x in self.order_ctypes.all()]
        pcl = "<br>".join(cl)
        return fh(pcl)

    class Meta:
        db_table = "orders_concrete"
        managed = True
        verbose_name = "concrete order"
        verbose_name_plural = "concrete orders"


class FootingsItem(models.Model):
    """adds footings information to the concrete order

    Args:
        order (int):    ForeignKey -> ConcreteOrder
        garage (char):  CharField
        wea (char):     CharField
    """

    order = models.ForeignKey(
        ConcreteOrder, verbose_name=_("order"), related_name="footings_items", on_delete=models.CASCADE
    )
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
    note = models.TextField(_("note"), blank=True, null=True)

    class Meta:
        db_table = "orders_concrete_order_footing_item"
        verbose_name = "footings item"
        verbose_name_plural = "footings items"
        managed = True
