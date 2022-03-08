from logging import PlaceHolder
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords as HR
from apps.core.models import ContactModel


class Supplier(ContactModel):

    name = models.CharField(_("Supplier Name"), max_length=50, unique=True)
    is_active = models.BooleanField(_("Active"), default=True)
    website = models.URLField(_("website"), max_length=200, blank=True, null=True)
    history = HR()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "suppliers"
        managed = True
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
