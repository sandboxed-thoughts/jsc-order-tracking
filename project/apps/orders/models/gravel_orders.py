from django.contrib import admin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.html import format_html as fh
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords as HR


class GravelOrder(models.Model):
    """Django model for gravel orders

    Fields:
        po          (str):      CharField
        priority    (str):      CharField
        builder     (int):      ForeignKey -> BuilderModel
        site        (str):      ForeignKey -> SiteModel
        lot         (int):      ForeignKey
        item        (int):      ForeignKey
        bsdt        (str):      CharField
        supplier    (int):      ForeignKey
        need_by     (datetime): DateField
        rloads      (int):      SmallIntegerField
        dloads      (int):      SmallIntegerField

    methods:
        nloads (int): returns the remaining loads to complete the order
        is_complete (bool): status
        get_lots (list): returns a list of lots formatted with line breaks
    """

    po = models.CharField(_("Purchase Order"), max_length=50, validators=[RegexValidator("[\\S\\w]")])
    priority = models.CharField(_("priority"), max_length=50)
    builder = models.ForeignKey(
        "clients.BuilderModel",
        verbose_name=_("builder"),
        related_name="builder_gravel_orders",
        limit_choices_to={"is_active": True},
        on_delete=models.PROTECT,
    )
    site = models.ForeignKey(
        "sites.SiteModel",
        verbose_name=_("site"),
        related_name="site_gravel_deliveries",
        limit_choices_to={"is_active": True},
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    lots = models.CharField(
        _("lots"), max_length=150, help_text='separate lots with a comma example: "1547, 78966, 251, 789665" '
    )
    item = models.ForeignKey("gravel.StoneType", verbose_name=_("stone type"), on_delete=models.PROTECT)
    bsdt = models.CharField(_("B/S D/T"), max_length=50, blank=True, null=True)
    supplier = models.ForeignKey("suppliers.Supplier", verbose_name=_("supplier"), on_delete=models.PROTECT)
    need_by = models.DateField(_("date needed"), auto_now=False, auto_now_add=False)
    rloads = models.SmallIntegerField(_("loads requested"))
    dloads = models.SmallIntegerField(_("loads delivered"), default=0)

    history = HR()

    class Meta:
        db_table = "orders_gravel"
        managed = True
        verbose_name = "Gravel Order"
        verbose_name_plural = "Gravel Orders"

    def __str__(self) -> str:
        return "{0} [{1}] for {2}".format(self.item, self.po, self.site)

    @admin.display(description="loads needed")
    def nloads(self) -> int:
        return self.rloads - self.dloads

    @admin.display(description="lots")
    def get_lots(self):
        ll = [x for x in self.lots.strip(" ").split(",")]
        pll = "<br>".join(ll)
        return fh(pll)

    def is_complete(self) -> bool:
        if self.nloads <= 0:
            return True
