from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..models  import ConcreteOrder, FlatworkItem, FlatworkOrder

class ConcreteOrderLot(models.Model):
    """Joins concrete orders to lots"""
    lot = models.ForeignKey("clients.Lot", verbose_name=_("lot"), on_delete=models.PROTECT)
    concrete_order = models.ForeignKey("ConcreteOrder", verbose_name=_("concrete order"), on_delete=models.PROTECT)

    class Meta:
        db_table = "concrete_order_lots"
        managed = True
        verbose_name = "concrete order lot"

class OrderInspection(models.Model):
    """Joins concrete orders to inspections"""
    concrete_order = models.ForeignKey("ConcreteOrder", verbose_name=_("concrete order"), on_delete=models.PROTECT)
    agency = models.ForeignKey("InspectionAgency", verbose_name=_("inspection agency"), on_delete=models.PROTECT)
    itime = models.DateTimeField(_("inspection time"), auto_now=False, auto_now_add=False)

    class Meta:
        db_table = "concrete_order_inspections"
        managed = True
        verbose_name = "concrete order inspection"

class FlatworkOrderItems(models.Model):
    """joins flatwork order with flatwork items"""
    flatwork_order = models.ForeignKey("FlatworkOrder", verbose_name=_("flatwork order"), on_delete=models.PROTECT)
    flatwork_item = models.ForeignKey("FlatworkItem", verbose_name=_("flatwork item"), on_delete=models.CASCADE)

    class Meta:
        db_table = "flatwork_concrete_order_items"
        managed = True
        verbose_name = "flatwork order items"

