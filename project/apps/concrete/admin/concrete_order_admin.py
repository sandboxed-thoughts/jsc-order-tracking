from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin as SHA

from ..models import (
    ConcreteOrder,
    FlatworkOrder,
    FlatworkItem,
    FlatworkOrderItems,
    WallOrder,
    FootingsOrder,
    ConcreteOrderInspection,
    InspectionAgency,
)


class FlatworkOrderItemsInline(admin.StackedInline):
    model = FlatworkOrderItems
    extra = 0
    min_num = 0


class ConcreteOrderInspectionInline(admin.StackedInline):
    model = ConcreteOrderInspection
    extra = 0
    min_num = 0


@admin.register(FlatworkOrder)
class FlatworkOrderAdmin(SHA):
    inlines = [
        FlatworkOrderItemsInline,
        ConcreteOrderInspectionInline,
    ]

    list_display = [
        "po",
        "supplier",
        "ctype",
        "dispatcher",
        "etotal",
        "qordered",
    ]

    fieldsets = (
        (None, {
            "fields": (
                "po",
                "ctype",
                "supplier",
                "dispatcher",
                "etotal",
                "atotal",
                "qordered",
                "order_date",
            ),
        }),
    )


@admin.register(FootingsOrder)
class FootingsOrderAdmin(SHA):

    inlines = [
        ConcreteOrderInspectionInline,
    ]

    list_display = [
        "po",
        "supplier",
        "ctype",
        "dispatcher",
        "etotal",
        "qordered",
    ]

    fieldsets = (
        (None, {
            "fields": (
                "po",
                "ctype",
                "supplier",
                "dispatcher",
                "etotal",
                "atotal",
                "qordered",
                "garage",
                "wea",
                "order_date",
            ),
        }),
    )


@admin.register(WallOrder)
class WallOrderAdmin(SHA):

    inlines = [
        ConcreteOrderInspectionInline,
    ]

    list_display = [
        "po",
        "supplier",
        "ctype",
        "dispatcher",
        "etotal",
        "qordered",
    ]

    fieldsets = (
        (None, {
            "fields": (
                "po",
                "ctype",
                "supplier",
                "dispatcher",
                "etotal",
                "atotal",
                "qordered",
                "order_date",
            ),
        }),
    )


@admin.register(FlatworkItem)
class FlatworkItemAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(InspectionAgency)
class InspectionAgencyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "get_addr",
        "phone",
        "email",
        "fax",
    ]
