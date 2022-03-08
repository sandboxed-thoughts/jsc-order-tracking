from django.db import models
from django.utils.html import format_html as fh
from django.utils.translation import gettext_lazy as _

from localflavor.us.models import USStateField as State, USZipCodeField as Zipcode
from simple_history.models import HistoricalRecords as HR


class JobSite(models.Model):
    name = models.CharField(_("Site Name"), max_length=100)
    street = models.CharField(_("Street Address"), max_length=50, blank=True, null=True)
    city = models.CharField(_("City"), max_length=50, blank=True, null=True)
    state = State(_("State"), blank=True, null=True)
    zipcode = Zipcode(_("Zip"), blank=True, null=True)
    is_active = models.BooleanField(_("Active"), default=True)
    history = HR()

    def __str__(self):
        return self.name

    def get_addr(self):
        if all[self.street, self.city, self.state, self.zipcode]:
            return fh(
                "<address>{0}<br/>{1}, {2}, {3}</address>".format(self.street, self.city, self.state, self.zipcode)
            )
        return self.pk

    class Meta:
        db_table = "job_sites"
        managed = True
        verbose_name = "Job Site"
        verbose_name_plural = "Job Sites"
