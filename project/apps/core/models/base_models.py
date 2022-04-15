from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from localflavor.us.models import USStateField as State, USZipCodeField as Zipcode
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords as HR

from .model_helpers import get_addr, get_untagged_addr


class AddressModel(models.Model):
    """
    The standard block of address information to any model

    Fields:
    ---
        street:     CharField
        city:       CharField
        state:      localflavor.us.models.USStateField
        zipcode:    localflavor.us.models.USZipCodeField

    Methods:
    ---
        get_addr:
            Returns the html version of the instance's complete addressor the id if an address cannot be created
    """

    street = models.CharField(_("Street Address"), max_length=50, blank=True, null=True)
    city = models.CharField(_("City"), max_length=50, blank=True, null=True)
    state = State(_("State"), blank=True, null=True)
    zipcode = Zipcode(_("Zip"), blank=True, null=True)

    @admin.display(description="address")
    def get_addr(self) -> str:
        return get_addr(self)

    def get_untagged_addr(self):
        return get_untagged_addr(self)

    def __str__(self):
        return self.get_addr

    class Meta:
        abstract = True


class ContactModel(models.Model):
    """
    The standard block of communications information to any model
    """

    phone = PhoneNumberField(_("Phone"), blank=True, null=True)
    fax = PhoneNumberField(_("Fax"), blank=True, null=True)
    email = models.EmailField(_("Email"), max_length=254, blank=True, null=True)

    def __str__(self):
        return self.pk

    class Meta:
        abstract = True


class CommunicationsModel(AddressModel, ContactModel):
    """
    Incorporates both, the address and contact models
    """

    def __str__(self):
        return self.get_addr

    class Meta:
        abstract = True


class NoteModel(models.Model):
    """Standard model for recording notes

    fields:
        author (int):           ForeignKey
        note (str):             TextField
        created_on (datetime):  DateTimeField
        updated_on (datetime):  DateTimeField
        history (obj):          HistoricalRecords
    """

    # user model
    User = settings.AUTH_USER_MODEL

    # fields
    author = models.ForeignKey(User, verbose_name=_("submitted by"), on_delete=models.CASCADE)
    note = models.TextField(
        _("Note"),
        max_length=250,
    )
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)

    history = HR(inherit=True)

    class Meta:
        abstract = True
