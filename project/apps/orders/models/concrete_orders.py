from django.conf import settings
from django.contrib import admin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.html import format_html as fh
from django.utils.translation import gettext_lazy as _

from apps.core.admin import get_notes
from apps.core.models import NoteModel
from simple_history.models import HistoricalRecords as HR

from ..helpers import GarageChoices, MixChoices, check_supplier_po, format_lots


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
        "clients.Client",
        verbose_name=_("builder"),
        related_name="builder_concrete_orders",
        on_delete=models.CASCADE,
    )
    site = models.ForeignKey(
        "clients.Site", verbose_name=_("site"), related_name="site_concrete_orders", on_delete=models.CASCADE
    )
    lots = models.CharField(
        _("lots"), max_length=150, help_text='separate each lot with a comma, ex "15446, 4789, 14,2546"'
    )
    needs_pump = models.BooleanField(_("pump required?"), default=False)
    etotal = models.SmallIntegerField(
        _("estimated total"),
    )
    atotal = models.SmallIntegerField(
        _("actual total"),
        blank=True,
        null=True,
    )
    qordered = models.SmallIntegerField(
        _("total ordered"),
        blank=True,
        null=True,
    )
    # order info
    date_needed = models.DateField(_("date needed"), auto_now=False, auto_now_add=False, blank=True, null=True)
    date_created = models.DateTimeField(_("created on"), auto_now=False, auto_now_add=True)
    supplier = models.ForeignKey(
        "supplies.Supplier",
        verbose_name=_("supplier"),
        related_name="supplier_concrete_orders",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    po = models.CharField(
        _("purchase order"),
        max_length=50,
        validators=[RegexValidator("[\\S\\w]")],
        blank=True,
        null=True,
        unique=True,
    )

    dispatcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("dispatcher"),
        related_name="corders_accepted",
        limit_choices_to={"groups__name": "Dispatchers"},
        on_delete=models.PROTECT,
    )
    # inspection = models.ForeignKey(
    #     InspectionModel, verbose_name=_("inspection"), on_delete=models.CASCADE, blank=True, null=True
    # )

    # history
    history = HR()

    def __str__(self) -> str:
        return "{0}".format(self.pk)

    objects = models.Manager()

    @admin.display(description="lots")
    def get_lots(self):
        return format_lots(self)

    @admin.display(description="", empty_value="")
    def get_notes(self):
        return get_notes(self.concrete_order_notes.all())

    @admin.display(description="concrete")
    def get_ctypes(self):
        if not self.concrete_supplies.first():
            return(fh('<span style="color: red">No concrete listed</span>'))
        cl = [x.__str__() for x in self.concrete_supplies.all()]
        pcl = "<br>".join(cl)
        return fh(pcl)

    def clean(self):
        check_supplier_po(self)
        super(ConcreteOrder, self).clean()

    class Meta:
        db_table = "orders_concrete"
        managed = True
        verbose_name = "concrete order"
        verbose_name_plural = "concrete orders"


class ConcreteOrderNote(NoteModel):

    order = models.ForeignKey(
        ConcreteOrder, verbose_name=_("concrete order"), related_name="concrete_order_notes", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "orders_concrete_order_notes"
        managed = True
        verbose_name = "order note"
        verbose_name_plural = "order notes"


class FlatworkItem(models.Model):
    order = models.ForeignKey(ConcreteOrder, verbose_name=_("order"), on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("item description"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "orders_concrete_flatwork_items"
        managed = True
        verbose_name = "flatwork item"
        verbose_name_plural = "flatwork items"


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
        max_length=4,
        blank=True,
        null=True,
    )
    wea = models.CharField(_("walkout egress area"), max_length=50, blank=True, null=True)
    note = models.TextField(_("additional information"), blank=True, null=True)

    class Meta:
        db_table = "orders_concrete_order_footing_item"
        verbose_name = "footings item"
        verbose_name_plural = "footings items"
        managed = True


class ConcreteType(models.Model):
    """Adds a concrete mix with included options to a concrete order

    Args:
        order   (int):  ForeignKey -> suppliers.ConcreteOrder
        mix     (str):  CharField
        slump   (str):  CharField
        note    (str):  TextField

    Methods:
        __str__ (str):  Returns a fractional display of mix over slump (m/s)
            example: "rich/5"
    """

    order = models.ForeignKey(
        ConcreteOrder,
        verbose_name=_("concrete orders"),
        related_name="concrete_supplies",
        on_delete=models.CASCADE,
    )
    mix = models.CharField(_("mix"), max_length=10, choices=MixChoices.choices, default=MixChoices.STANDARD)
    slump = models.CharField(_("slump"), max_length=6)
    note = models.TextField(_("note"), blank=True, null=True, max_length=250)

    def __str__(self):
        return "{0}/{1}".format(self.mix, self.slump)

    class Meta:
        db_table = "supplies_concrete_types"
        managed = True
        verbose_name = "Concrete Type"
        verbose_name_plural = "Concrete Types"
