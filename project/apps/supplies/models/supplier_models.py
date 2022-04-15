from django.contrib import admin
from django.db import models
from django.utils.html import format_html as fh
from django.utils.translation import gettext_lazy as _

from apps.core.models import CommunicationsModel
from simple_history.models import HistoricalRecords as HR

from ..managers import ActiveSuppliers, ConcreteSupplier, GravelSupplier, PumpRentalSupplier


class Supplier(CommunicationsModel):
    """Supplier model

    Args:
        name            (str):          CharField
        is_active       (bool):         BooleanField
        website         (str):          URLField
        created_on      (datetime):     DateTimeField
        updated_on      (datetime):     DateTimeField
        has_gravel      (bool):         BooleanField
        has_pump        (bool):         BooleanField
        has_concrete    (bool):         BooleanField
        history         (class):        Historical Record

        get_site        (str):          returns html link to website

    Managers:
        objects             (queryset):     returns all Supplier objects
        active_suppliers    (queryset):     returns Supplier.objects.all().filter(is_active = True)
        pump_suppliers      (queryset):     returns Supplier.active_suppliers.all().filter(has_pump = True)
        gravel_suppliers    (queryset):     returns Supplier.active_suppliers.all().filter(has_gravel = True)
        concrete_suppliers  (queryset):     returns Supplier.active_suppliers.all().filter(has_concrete = True)
    """

    name = models.CharField(_("Supplier Name"), max_length=50, unique=True)
    is_active = models.BooleanField(_("Active"), default=True)
    website = models.URLField(_("website"), max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(_("created on"), auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True, auto_now_add=False)
    # supply types
    has_gravel = models.BooleanField(_("supplies gravel"), default=False)
    has_concrete = models.BooleanField(_("supplies concrete"), default=False)
    has_pump = models.BooleanField(_("rents pumps"), default=False)
    # history
    history = HR(inherit=True)

    # model managers
    objects = models.Manager()
    active_suppliers = ActiveSuppliers()
    gravel_suppliers = GravelSupplier()
    concrete_suppliers = ConcreteSupplier()
    pump_suppliers = PumpRentalSupplier()

    def __str__(self):
        return self.name.title()

    @admin.display(description="view site")
    def get_site(self) -> str:
        """returns the formatted anchor to open the listed website"""
        if self.website is not None:
            return fh('<a href="{0}" target="blank">{0}</a>'.format(self.website))
        return "none provided"

    class Meta:
        db_table = "supplies_suppliers"
        managed = True
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
