from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html as fh
from simple_history.models import HistoricalRecords as HR


class Concrete(models.Model):

    """
    Concrete order tracking model.
    """

    WALLS = "walls"
    FLATWORK = "flatwork"
    FOOTINGS = "footings"
    RAIN = "rain"
    SNOW = "snow"
    NONE = "none"
    LOW = "low"
    HIGH = "high"
    AVERAGE = "none"
    MIX = "mix"
    SLUMP = "slmp"
    WILL_CALL = "w/c"
    CANCELED = "cncl"
    RELEASED = "rlsd"
    COMPLETE = "complete"

    ORDER_TYPE_CHOICES = [
        (WALLS, "walls"),
        (FLATWORK, "flatwork"),
        (FOOTINGS, "footings"),
    ]
    WEATHER_CHOICES = [
        (RAIN, "rain"),
        (SNOW, "snow"),
        (NONE, "none"),
    ]
    TEMP_CHOICES = [
        (LOW, "low"),
        (HIGH, "high"),
        (AVERAGE, "average"),
    ]
    C_TYPE_CHOICES = [
        (MIX, "mix"),
        (SLUMP, "slmp"),
    ]
    PROGRESS_CHOICES = [
        (WILL_CALL, "w/c"),
        (CANCELED, "cncl"),
        (RELEASED, "rlsd"),
        (COMPLETE, "complete"),
    ]

    otype = models.CharField(
        _("Pour Type"),
        max_length=8,
        choices=ORDER_TYPE_CHOICES,
    )
    pdate = models.DateField(
        _("Pour Date"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    incw = models.CharField(
        _("Inclimate Weather"), max_length=4, choices=WEATHER_CHOICES, default=NONE
    )
    temp = models.CharField(
        _("Temperature"), max_length=4, choices=TEMP_CHOICES, default=AVERAGE
    )
    bldr = models.CharField(_("Builder"), max_length=50)
    job_site = models.CharField(_("Job Site"), max_length=50)
    lot = models.CharField(
        _("Lot Numbers"), max_length=100, help_text="separate each lot with a comma (,)"
    )
    item = models.CharField(_("Item"), max_length=50)
    cpour = models.CharField(_("Crew Pouring"), max_length=150, blank=True, null=True)
    supplier = models.CharField(_("Supplier"), max_length=50)
    dsph = models.CharField(_("Dispatcher"), max_length=50)
    ono = models.PositiveIntegerField(
        _("Order Number"),
    )
    etot = models.PositiveIntegerField(
        _("Estimated Total"),
    )
    qord = models.PositiveIntegerField(
        _("Quantity Ordered"),
    )
    atot = models.PositiveIntegerField(_("Actual Total"), blank=True, null=True)
    ctype = models.CharField(_("Mix/Slump"), max_length=4, choices=C_TYPE_CHOICES)
    pump = models.BooleanField(_("Pump"), default=False)
    pinfo = models.CharField(_("Pump Info"), max_length=150, blank=True, null=True)
    iagt = models.CharField(
        _("Inspection Agency"), max_length=50, blank=True, null=True
    )
    itime = models.DateTimeField(
        _("Inspection Time"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    ctime = models.DateTimeField(
        _("Concrete Time"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    pprog = models.CharField(
        _("Pour Progress"), max_length=8, choices=PROGRESS_CHOICES, default=WILL_CALL
    )
    history = HR()
    garage = models.CharField(
        _("Garage Height"),
        max_length=3,
        default="n/a",
        blank=True,
        null=True,
        help_text="only for footings",
    )
    wea = models.CharField(
        _("Walkout Egress Area"),
        max_length=50,
        default="n/a",
        blank=True,
        null=True,
        help_text="only for footings",
    )

    def get_lots(self):
        ll = [x for x in self.lot.strip(" ").split(",")]
        pll = "<br>".join(ll)
        return fh(pll)

    def __str__(self) -> str:
        return "{0} [{1}] {2}".format(self.job_site, self.lot, self.pk)

    class Meta:
        db_table = "c_orders"
        managed = True
        verbose_name = "Concrete Order"
        verbose_name_plural = "Concrete Orders"


class ConcreteNote(models.Model):
    order = models.ForeignKey(
        Concrete,
        verbose_name=_("Order Note"),
        related_name="c_order",
        on_delete=models.CASCADE,
    )
    note = models.TextField(_("Note"))
    created_on = models.DateTimeField(
        _("note added on"), auto_now=True, auto_now_add=False
    )
    updated_on = models.DateTimeField(
        _("note last updated"), auto_now=False, auto_now_add=True
    )
    history = HR()

    def __str__(self):
        return "note for {}".format(self.order.__str__())

    class Meta:
        db_table = "c_order_notes"
        managed = True
        verbose_name = "Concrete Note"
        verbose_name_plural = "Concrete Notes"
