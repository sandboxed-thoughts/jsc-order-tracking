from django.contrib import admin

# from apps.core.admin import activate, deactivate, get_change, get_history
from apps.orders.models import Concrete
from simple_history.admin import SimpleHistoryAdmin as SHA

# from django.utils.html import format_html as fh



@admin.register(Concrete)
class ConcreteAdmin(SHA):
    pass
