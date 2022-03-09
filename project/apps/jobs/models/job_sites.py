from django.contrib import admin
from django.db import models
from django.utils.html import format_html as fh
from django.utils.translation import gettext_lazy as _

from localflavor.us.models import USStateField as State, USZipCodeField as Zipcode
from simple_history.models import HistoricalRecords as HR


class JobSite(models.Model):
    """
    Customer worksites
    
    Fields:
        name:       CharField,
        street:     CharField,
        city:       CharField,
        state:      localflavor.us.models.USStateField,
        zipcode:    localflavor.us.models.USZipCodeField,
    
    Methods:
        get_addr:   returns the instance's full formatted address as html,
    """    
    
    name = models.CharField(_("Site Name"), max_length=100)
    street = models.CharField(_("Street Address"), max_length=50, blank=True, null=True)
    city = models.CharField(_("City"), max_length=50, blank=True, null=True)
    state = State(_("State"), blank=True, null=True)
    zipcode = Zipcode(_("Zip"), blank=True, null=True)
    is_active = models.BooleanField(_("Active"), default=True)
    history = HR()

    def __str__(self):
        return self.name

    @admin.display(description="address")
    def get_addr(self) -> str:
        # returns the instance's full formatted address as html
        parts = [self.street, "<br>", self.city, self.state, self.zipcode]
        if any(parts):
            count = len(parts) - 1
            address = "<address>"
            for k, v in enumerate(parts):
                if v is not None:
                    address += v.capitalize()
                if v == self.city and self.city is not None:
                    address += ", "
                elif 2 <= k < count:
                    address += " "
            address += "</address>"
            return fh(address)
        return "not provided"

    class Meta:
        db_table = "job_sites"
        managed = True
        verbose_name = "Job Site"
        verbose_name_plural = "Job Sites"
