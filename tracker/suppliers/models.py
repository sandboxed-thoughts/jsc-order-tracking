from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords as HR

from core.models import ContactModel

# Create your models here.


class Supplier(
    ContactModel,
):
    name = models.CharField(_("Name"), max_length=75)
    is_active = models.BooleanField(_("Active"), default=True)
    history = HR()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "suppliers"
        managed = True
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"


class Item(models.Model):
    name = models.CharField(_("Item Name"), max_length=50)
    suppliers = models.ManyToManyField(Supplier, verbose_name=_("Suppliers"), related_name="Items")
    history = HR()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
