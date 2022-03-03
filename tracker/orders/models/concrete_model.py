from django.db import models
from django.utils.html import format_html as fh
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords as HR


class Concrete(models.Model):

    """
    Concrete order tracking model.
    """

    # choices
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
        (FLATWORK, "flatwork"),
        (FOOTINGS, "footings"),
        (WALLS, "walls"),
    ]
    WEATHER_CHOICES = [
        (NONE, "none"),
        (RAIN, "rain"),
        (SNOW, "snow"),
    ]
    TEMP_CHOICES = [
        (AVERAGE, "average"),
        (LOW, "low"),
        (HIGH, "high"),
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

    # fields
    otype = models.CharField(
        _("Pour Type"),
        max_length=8,
        choices=ORDER_TYPE_CHOICES,
    )
    pdate = models.DateField(_("Pour Date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    incw = models.CharField(_("Inclimate Weather"), max_length=4, choices=WEATHER_CHOICES, default=NONE)
    temp = models.CharField(_("Temperature"), max_length=4, choices=TEMP_CHOICES, default=AVERAGE)
    bldr = models.CharField(_("Builder"), max_length=50)
    job_site = models.CharField(_("Job Site"), max_length=50)
    lot = models.CharField(_("Lot Numbers"), max_length=100, help_text="separate each lot with a comma (,)")
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
    pinfo = models.TextField(_("Pump Info"), max_length=150, blank=True, null=True)
    iagt = models.CharField(_("Inspection Agency"), max_length=50, blank=True, null=True)
    itime = models.DateTimeField(_("Inspection Time"), auto_now=False, auto_now_add=False, blank=True, null=True)
    ctime = models.DateTimeField(_("Concrete Time"), auto_now=False, auto_now_add=False, blank=True, null=True)
    pprog = models.CharField(_("Pour Progress"), max_length=8, choices=PROGRESS_CHOICES, default=WILL_CALL)
    history = HR()
    garage = models.PositiveSmallIntegerField(
        _("Garage Height (ft)"), blank=True, null=True, help_text="only for footings"
    )
    wea = models.PositiveSmallIntegerField(
        _("Walkout Egress Area (ft)"), blank=True, null=True, help_text="only for footings"
    )
    notes = models.TextField(
        _("order notes"),
        blank=True,
        null=True,
    )

    def get_lots(self):
        return fh("<br>".join([x for x in self.lot.strip().split(",")]))

    def __str__(self) -> str:
        return "{0} [{1}] {2}".format(self.job_site, self.lot, self.pk)

    class Meta:
        db_table = "c_orders"
        managed = True
        verbose_name = "Concrete Order"
        verbose_name_plural = "Concrete Orders"
