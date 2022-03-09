from django.contrib import admin
from django.utils.html import format_html as fh
from simple_history.admin import SimpleHistoryAdmin as SHA
from apps.core.admin import deactivate, activate, get_change, get_history
from apps.orders.models import Concrete


@admin.register(Concrete)
class ConcreteAdmin(SHA):
    pass
