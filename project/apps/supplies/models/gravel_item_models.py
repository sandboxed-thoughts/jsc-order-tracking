from django.db import models
from django.utils.translation import gettext_lazy as _


class GravelItem(models.Model):
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
        db_table = "supplies_gravel_items"
        managed = True
        verbose_name = "Stone Type"
        verbose_name_plural = "Stone Types"
