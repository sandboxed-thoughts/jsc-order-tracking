from django.db import models
from django.utils.translation import gettext_lazy as _

from localflavor.us.models import USStateField as State, USZipCodeField as Zipcode
from phonenumber_field.modelfields import PhoneNumberField


class ContactModel(models.Model):
    """Abstract model to include the standard block of contact information to any model"""

    street = models.CharField(_("Street Address"), max_length=50, blank=True, null=True)
    city = models.CharField(_("City"), max_length=50, blank=True, null=True)
    state = State(_("State"), blank=True, null=True)
    zipcode = Zipcode(_("Zip"), blank=True, null=True)
    phone = PhoneNumberField(_("Phone"), blank=True, null=True)
    email = models.EmailField(_("Email"), max_length=254, blank=True, null=True)
    fax = models.PhoneNumberField(_("Fax"), blank=True, null=True)

    class Meta:
        abstract = True
