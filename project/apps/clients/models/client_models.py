from gettext import translation
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import ContactModel, AddressModel
from simple_history.models import HistoricalRecords as HR

class Builder(ContactModel):

    class Meta:
        db_table = 'client_builders'
        managed = True
        verbose_name = 'Builder'
        verbose_name_plural = 'Builders'

    name = models.CharField(_("name"), max_length = 150, unique=True)
    is_active = models.BooleanField(_("active builder"), default=True,)
    history = HR()

    def __str__(self) -> str:
        return self.name.title()


class Subdivision(AddressModel):
    """
    Customer worksites

    Fields:
        name:       CharField,
        street:     None,
        city:       CharField,
        state:      localflavor.us.models.USStateField,
        zipcode:    localflavor.us.models.USZipCodeField,

    Methods:
        get_addr:   returns the instance's full formatted address as html,
    """

    class Meta:
        db_table = "client_subdivision"
        managed = True
        verbose_name = "Subdivision"
        verbose_name_plural = "Subdivisions"

    name = models.CharField(_("Site Name"), max_length=100)
    is_active = models.BooleanField(_("Active"), default=True)
    history = HR()

    def __str__(self):
        return self.name 

class Lot(models.Model):

    class Meta:
        db_table = 'client_lots'
        managed = True
        verbose_name = 'Lot'
        verbose_name_plural = 'Lots'


    name = models.CharField(_("lot"), max_length=50)
    builder = models.ForeignKey(Builder, verbose_name=_("builder"), related_name='builder_lots', on_delete=models.PROTECT)
    subdivision = models.ForeignKey(Subdivision, verbose_name=_("subdivision"), on_delete=models.PROTECT)
    history = HR(inherit=True)

    def __str__(self):
        return "{0}: {1} {2}".format(self.builder, self.name, self.subdivision)
