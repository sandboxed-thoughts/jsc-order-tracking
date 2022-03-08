from django.contrib import admin

from .models import Gravel, Concrete

from simple_history.admin import SimpleHistoryAdmin as SHA


@admin.register(Gravel)
class GravelAdmin(SHA):
    pass


@admin.register(Concrete)
class ConcreteAdmin(SHA):
    pass
