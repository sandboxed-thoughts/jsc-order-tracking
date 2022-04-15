from django.contrib import admin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.admin import get_notes
from apps.core.models import NoteModel
from simple_history.models import HistoricalRecords as HR

from ..helpers import OrderStatusChoices, check_supplier_po, format_lots


class GravelOrderNote(NoteModel):
    """Notes for gravel orders

    Args:
        NoteModel   (object):   author, note, created_on, updated_on
        order       (int):      ForeignKey -> orders.GravelOrder
    """

    order = models.ForeignKey(
        "GravelOrder",
        verbose_name=_("gravel order"),
        related_name="gravel_order_notes",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "orders_gravel_order_notes"
        managed = True
        verbose_name = "order note"
        verbose_name_plural = "order notes"


class GravelOrder(models.Model):
    """Django model for gravel orders

    Fields:
        priority    (str):      CharField
        builder     (int):      ForeignKey -> clients.Client
        site        (str):      ForeignKey -> clients.Site
        lot         (str):      CharField
        item        (int):      ForeignKey -> supplies.GravelItem
        bsdt        (str):      CharField
        supplier    (int):      ForeignKey -> supplies.Supplier
        po          (str):      CharField
        need_by     (datetime): DateField
        rloads      (int):      SmallIntegerField
        dloads      (int):      SmallIntegerField

    methods:
        nloads (int): returns the remaining loads to complete the order
        is_complete (bool): status
        get_lots (list): returns a list of lots formatted with line breaks
    """

    priority = models.CharField(_("priority"), max_length=50, blank=True, null=True)
    builder = models.ForeignKey(
        "clients.Client",
        verbose_name=_("builder"),
        related_name="builder_gravel_orders",
        limit_choices_to={"is_active": True},
        on_delete=models.PROTECT,
    )
    site = models.ForeignKey(
        "clients.Site",
        verbose_name=_("site"),
        related_name="site_gravel_deliveries",
        limit_choices_to={"is_active": True},
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    lots = models.CharField(
        _("lots"),
        max_length=150,
        help_text='separate lots with a comma. Example: "1547 Cherrywood St, 1549 Cherrywood St, 2867 Flintwood Cir',
    )
    item = models.ForeignKey(
        "supplies.GravelItem",
        verbose_name=_("item"),
        on_delete=models.PROTECT,
        related_name="gravel_order_items",
    )
    bsdt = models.CharField(
        _("B/S D/T"),
        max_length=3,
        choices=[("b/s", "b/s"), ("d/t", "d/t")],
    )
    supplier = models.ForeignKey(
        "supplies.Supplier",
        verbose_name=_("supplier"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    po = models.CharField(
        _("purchase order"),
        max_length=150,
        validators=[RegexValidator("[[\\S\\w]")],
        blank=True,
        null=True,
    )
    need_by = models.DateField(
        _("date needed"),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    rloads = models.SmallIntegerField(
        _("loads requested"),
        blank=True,
        null=True,
    )
    dloads = models.SmallIntegerField(
        _("loads delivered"),
        default=0,
    )
    status = models.CharField(
        _("status"),
        max_length=10,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING,
    )
    history = HR()

    class Meta:
        db_table = "orders_gravel"
        managed = True
        verbose_name = "gravel order"
        verbose_name_plural = "gravel orders"

    def __str__(self):
        return "{0}".format(self.pk)

    @admin.display(description="loads needed")
    def nloads(self) -> int:
        if self.rloads and self.dloads:
            return self.rloads - self.dloads
        return "cannot compute"

    @admin.display(description="lots")
    def get_lots(self):
        return format_lots(self)

    @admin.display(description="", empty_value="")
    def get_notes(self):
        return get_notes(self.gravel_order_notes.all().order_by("created_on"))

    def clean(self):
        check_supplier_po(self)
        super(GravelOrder, self).clean()
