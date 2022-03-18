from django.db import models
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords as HR
from ..helpers import MixChoices


class StoneType(models.Model):
    """Various orderable types of gravel"""

    name = models.CharField(
        _("Stone Type"),
        max_length=50,
        unique=True,
    )
    description = models.TextField(_("Description"), max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name.title()

    class Meta:
        db_table = "suppliers_gravelitems"
        managed = True
        verbose_name = "Stone Type"
        verbose_name_plural = "Stone Types"


class ConcreteType(models.Model):
    """Various orderable types of concrete"""

    name = models.CharField(
        _("Concrete Type"),
        max_length=50,
        unique=True,
    )
    mix = models.CharField(_("mix"), max_length=10, choices=MixChoices.choices, default=MixChoices.STANDARD)
    slump = models.CharField(_("slump"), max_length=6)
    description = models.TextField(_("Description"), max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "suppliers_concreteitems"
        managed = True
        verbose_name = "Concrete Type"
        verbose_name_plural = "Concrete Types"
