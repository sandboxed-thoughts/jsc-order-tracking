from django.db import models
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords as HR


class StoneType(models.Model):
    name = models.CharField(
        _("Stone Type"),
        max_length=50,
        unique=True,
    )
    description = models.TextField(_("Description"), max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "stone_types"
        managed = True
        verbose_name = "Stone Type"
        verbose_name_plural = "Stone Types"
