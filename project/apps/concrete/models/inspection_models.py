from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords as HR
from apps.core.models import ContactModel

class InspectionAgency(ContactModel):
    name = models.CharField(_("agency name"), max_length=50,unique=True)

    def __str__(self):
        return self.name.title()

    class Meta:
        db_table = "inspection_agency"
        managed = True
        verbose_name = "inspection agency"
        verbose_name_plural = "inspection agencies"