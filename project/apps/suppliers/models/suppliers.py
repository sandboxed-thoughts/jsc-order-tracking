from django.contrib import admin
from django.db import models
from django.utils.html import format_html as fh
from django.utils.translation import gettext_lazy as _

from apps.core.models import ContactModel
from simple_history.models import HistoricalRecords as HR


class Supplier(ContactModel):

    name = models.CharField(_("Supplier Name"), max_length=50, unique=True)
    is_active = models.BooleanField(_("Active"), default=True)
    website = models.URLField(_("website"), max_length=200, blank=True, null=True)
    history = HR(inherit=True)

    def __str__(self):
        return self.name

    @admin.display(description="view site")
    def get_site(self) -> str:
        if self.website is not None:
            return fh('<a href="{0}" target="blank">{0}</a>'.format(self.website))
        return "none provided"

    class Meta:
        db_table = "suppliers"
        managed = True
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
