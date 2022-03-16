from django.contrib import admin
from ..models import ConcreteOrder, FlatworkOrderItems
from simple_history.admin import SimpleHistoryAdmin as SHA


@admin.register(ConcreteOrder)
class ConcreteOrderAdmin(SHA):
    pass
