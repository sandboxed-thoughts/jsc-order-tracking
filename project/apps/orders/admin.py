from django.contrib import admin

from .models import Gravel, Concrete

from simple_history.admin import SimpleHistoryAdmin as SHA


@admin.register(Gravel)
class GravelAdmin(SHA):
    list_display = [
        "po",
        "supplier",
        "progress",
        "job_site",
        "get_lots",
        "ndate",
    ]


@admin.register(Concrete)
class ConcreteAdmin(SHA):
    pass
