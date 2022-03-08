from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html as fh
from localflavor.us.models import USStateField as State, USZipCodeField as Zipcode
from phonenumber_field.modelfields import PhoneNumberField


class ContactModel(models.Model):
    """
    The standard block of contact information to any model

    Fields:
    ---
        street: CharField
        city:   CharField
        state:  localflavor.us.models.USStateField
        phone:  phonenumber_field.modelfields.PhoneNumberField
        fax:    phonenumber_field.modelfields.PhoneNumberField
        email:  EmailField

    Methods:
    ---
        get_addr:
            Returns the html version of the instance's complete addressor the id if an address cannot be created
    """

    street = models.CharField(_("Street Address"), max_length=50, blank=True, null=True)
    city = models.CharField(_("City"), max_length=50, blank=True, null=True)
    state = State(_("State"), blank=True, null=True)
    zipcode = Zipcode(_("Zip"), blank=True, null=True)
    phone = PhoneNumberField(_("Phone"), blank=True, null=True)
    fax = PhoneNumberField(_("Fax"), blank=True, null=True)
    email = models.EmailField(_("Email"), max_length=254, blank=True, null=True)

    def get_addr(self):
        return fh("<address>{0}<br/>{1}, {2}, {3}</address>".format(self.street, self.city, self.state, self.zipcode))
        
    def __str__(self):
        return self.get_addr

    class Meta:
        abstract = True
