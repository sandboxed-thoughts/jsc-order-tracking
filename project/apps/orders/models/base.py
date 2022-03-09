from django.contrib import admin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.html import format_html as fh
from django.utils.translation import gettext_lazy as _


class BaseOrder(models.Model):
    """The base fields and model methods for an order

    Fields:
        bldr (str): A person or crew performing the work
        lot (str): A string of comma-separated lot numbers
        incw (str): A choice of order delays based on inclimate weather
        temp (str): A choice of order delays based on temperature
        odate (datetime): The date the order was placed
        po(str): The purchase order or order number
        progress(str): A choice of order progress
        notes(str): Comments about the order
        is_complete (bool): True if rloads equals dloads

    Methods:
        get_lots: Returns the list of lots in an html format with line breaks
            between the different lot numbers
    """

    # choices

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
            (CANCELED, "canceled"),
            (RELEASED, "released"),
            (COMPLETE, "complete"),
        ]

    # fields
    bldr = models.CharField(_("Builder"), max_length=50)
    lot = models.CharField(_("Lot Numbers"), max_length=100, help_text="separate multiple lots with a comma (,)")
    incw = models.CharField(
        _("Inclimate Weather"), max_length=4, choices=WeatherChoices.choices, default=WeatherChoices.NONE
    )
    temp = models.CharField(_("Temperature"), max_length=7, choices=TempChoices.choices, default=TempChoices.AVERAGE)
    odate = models.DateField(_("Date Ordered"), auto_now=False, auto_now_add=False, editable=True)
    po = models.CharField(
        _("Purchase Order"), max_length=50, help_text="PO / order number", validators=[RegexValidator("[\\S\\w]")]
    )
    progress = models.CharField(
        _("Order Progress"), max_length=10, choices=ProgressChoices.choices, default=ProgressChoices.WILL_CALL
    )
    notes = models.TextField(_("notes"), blank=True, null=True)
    is_complete = models.BooleanField(_("Order Complete"), default=False)

    @admin.display(description="lots")
    def get_lots(self):
        """Returns an html-formatted list of lots from the lot field"""
        return fh("<br>".join([x for x in self.lot.strip().split(",")]))

    def __str__(self) -> str:
        return "{0} [{1}] {2}".format(self.job_site, self.lot, self.pk)

    class Meta:
        abstract = True
