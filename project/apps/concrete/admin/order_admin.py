from django.contrib import admin

from apps.core.admin import get_change, get_history
from simple_history.admin import SimpleHistoryAdmin as SHA

from ..forms import BaseConcreteOrderForm
from ..models import PumpInfo, ConcreteOrder, WallOrder, FlatworkOrder, FootingsOrder


class FlatworkOrderInline(admin.TabularInline):
    '''Tabular Inline View for FlatworkOrder'''

    model = FlatworkOrder
    extra = 0
    min_num = 0
    max_num = 1

class FootingsOrderInline(admin.TabularInline):
    '''Tabular Inline View for FootingsOrder'''

    model = FootingsOrder
    extra = 0
    min_num = 0
    max_num = 1

class WallOrderInline(admin.TabularInline):
    '''Tabular Inline View for WallOrder'''

    model = WallOrder
    extra = 0
    min_num = 0
    max_num = 1

class PumpInfoInline(admin.StackedInline):
    """Tabular Inline View for PumpInfo"""
    model = PumpInfo
    extra = 1
    min_num = 0
    max_num = 1


@admin.register(ConcreteOrder)
class ConcreteOrderAdmin(SHA):
    inlines = [PumpInfoInline,FlatworkOrderInline,FootingsOrderInline, WallOrderInline,]

@admin.register(FlatworkOrder)
class FlatworkOrderAdmin(SHA):
    pass

@admin.register(FootingsOrder)
class FootingsOrderAdmin(SHA):
    pass

@admin.register(WallOrder)
class WallOrderAdmin(SHA):
    pass