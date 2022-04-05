from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import ContactModel
from simple_history.models import HistoricalRecords as HR


class InspectionModel(ContactModel):
    name = models.CharField(_("agency name"), max_length=50)
    agent = models.CharField(_("inspector name"), max_length=50)
    inspection_date = models.DateTimeField(_("inspection time"), auto_now=False, auto_now_add=False)
    note = models.TextField(_("note"), max_length=250, blank=True, null=True)
    history = HR()

    def __str__(self):
        return self.name.title()

    class Meta:
        db_table = "orders_inspection_agency"
        managed = True
        verbose_name = "inspection agency"
        verbose_name_plural = "inspection agencies"


class ConcreteInspection(InspectionModel):
    order = models.ForeignKey("orders.ConcreteOrder", verbose_name=_("concrete order"), on_delete=models.CASCADE)

    db_table = "orders_concrete_inspections"
    managed = True
