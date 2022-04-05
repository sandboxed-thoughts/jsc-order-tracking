from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import ConcreteType


class ConcreteTypeInline(admin.StackedInline):
    """Stacked Inline View for ConcreteType"""

    model = ConcreteType
    min_num = 0
    max_num = 20
    extra = 0


@admin.register(ConcreteType)
class ConcreteTypeAdmin(SHA):
    pass
