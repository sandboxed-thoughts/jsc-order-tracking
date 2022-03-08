from django.db import models
from django.contrib import admin
from django.utils.html import format_html as fh
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from simple_history.models import HistoricalRecords as HR


class BaseOrder(models.Model):
    """The base fields and model methods for an order

    Fields:
        bldr:       CharField
        job_site:   ForeignKey
        lot:        CharField
        qord:       PositiveIntegerField
        qtype:      CharField
        etot:       PositiveIntegerField
        atot:       PositiveIntegerField
        incw:       CharField
        temp:       CharField
        notes:      TextField
        odate:      DateField
        ndate:      DateField
        ddate:      DateField
        po:         CharField
        progress:   CharField
    """

    # choices
    class QTypeChoices:
        LOADS = "loads"
        CUYD = "cu yd"
        SQFT = "sqft"
        LBS = "lbs"
        BAGS = "bags"

        choices = [
            (
                "Large Loads",
                (
                    (LOADS, "loads"),
                    (CUYD, "cu yd"),
                    (SQFT, "sqft"),
                ),
            ),
            (LBS, "lbs"),
            (BAGS, "bags"),
        ]

    class WeatherChoices:
        NONE = "none"
        RAIN = "rain"
        SNOW = "snow"

        choices = [
            (NONE, "none"),
            (RAIN, "rain"),
            (SNOW, "snow"),
        ]

    class TempChoices:
        AVERAGE = "average"
        LOW = "low"
        HIGH = "high"

        choices = [
            (AVERAGE, "average"),
            (LOW, "low"),
            (HIGH, "high"),
        ]
        WILL_CALL = "w/c"

    class ProgressChoices:
        WILL_CALL = "will call"
        SCHEDULED = "scheduled"
        CANCELED = "canceled"
        RELEASED = "released"
        COMPLETE = "complete"

        choices = [
            (WILL_CALL, "will call"),
            (SCHEDULED, "scheduled"),
            (CANCELED, "cncl"),
            (RELEASED, "rlsd"),
            (COMPLETE, "complete"),
        ]

    # fields
    bldr = models.CharField(_("Builder"), max_length=50)
    lot = models.CharField(_("Lot Numbers"), max_length=100, help_text="separate multiple lots with a comma (,)")
    supplier = models.ForeignKey("suppliers.Supplier", verbose_name=_("Supplier"), on_delete=models.CASCADE)
    item = models.CharField(_("Item"), max_length=50)
    qord = models.PositiveIntegerField(
        _("Quantity Ordered"),
    )
    qtype = models.CharField(
        _("Quantity Type"), max_length=5, choices=QTypeChoices.choices, default=QTypeChoices.LOADS
    )
    etot = models.PositiveIntegerField(_("Estimated Total"), help_text="leave blank if same as quantity ordered")
    atot = models.PositiveIntegerField(_("Actual Total"), blank=True, null=True)
    incw = models.CharField(
        _("Inclimate Weather"), max_length=4, choices=WeatherChoices.choices, default=WeatherChoices.NONE
    )
    temp = models.CharField(_("Temperature"), max_length=7, choices=TempChoices.choices, default=TempChoices.AVERAGE)
    odate = models.DateField(_("Date Ordered"), auto_now=True, auto_now_add=False)
    ndate = models.DateField(_("Date Needed"), auto_now=False, auto_now_add=False, blank=True, null=True)
    ddate = models.DateField(_("Delivery / Pour Date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    crew = models.CharField(_("Delivery / Pour Crew"), max_length=50, blank=True, null=True)
    po = models.CharField(
        _("Purchase Order"), max_length=50, help_text="PO / order number", validators=[RegexValidator("[\S\w]")]
    )
    progress = models.CharField(
        _("Order Progress"), max_length=10, choices=ProgressChoices.choices, default=ProgressChoices.WILL_CALL
    )
    notes = models.TextField(_("notes"), blank=True, null=True)

    @admin.display(description="lots")
    def get_lots(self):
        return fh("<br>".join([x for x in self.lot.strip().split(",")]))

    def __str__(self) -> str:
        return "{0} [{1}] {2}".format(self.job_site, self.lot, self.pk)

    class Meta:
        abstract = True
