from django.contrib import admin
from apps.core.admin import get_change, get_history
from simple_history.admin import SimpleHistoryAdmin as SHA
from ..forms import BaseConcreteOrderForm
from ..models import ConcreteOrder


@admin.register(ConcreteOrder)
class ConcreteOrderAdmin(SHA):
    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = BaseConcreteOrderForm
        return super().get_form(request, obj, **kwargs)