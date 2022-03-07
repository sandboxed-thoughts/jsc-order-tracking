from django.contrib import admin

from .models import Supplier, Item


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    filter_horizontal = ["suppliers"]
