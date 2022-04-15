from django.db.models import Manager
from django.utils.translation import gettext_lazy as _


class ActiveSuppliers(Manager):
    """Gets only the suppliers that are active"""

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class PumpRentalSupplier(ActiveSuppliers):
    """Gets only the suppliers that have pumps"""

    def get_queryset(self):
        return super().get_queryset().filter(has_pump=True)


class GravelSupplier(ActiveSuppliers):
    """Gets only the suppliers that have gravel"""

    def get_queryset(self):
        return super().get_queryset().filter(has_gravel=True)


class ConcreteSupplier(ActiveSuppliers):
    """Gets only the suppliers that have concrete"""

    def get_queryset(self):
        return super().get_queryset().filter(has_concrete=True)
