from django.db import models
from django.utils.translation import gettext_lazy as _


class FlatworkOrderItems(models.Model):
    """joins flatwork order with flatwork items"""

    concrete_order = models.ForeignKey(
        "ConcreteOrder",
        verbose_name=_("concrete order"),
        related_name="flatwork_items",
        related_query_name="order_item",
        on_delete=models.PROTECT,
    )
    flatwork_item = models.ForeignKey(
        "FlatworkItem",
        verbose_name=_("flatwork item"),
        related_name="item_orders",
        related_query_name="item_order",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "orders_concrete_flatwork_order_items"
        managed = True
        verbose_name = "flatwork item"
