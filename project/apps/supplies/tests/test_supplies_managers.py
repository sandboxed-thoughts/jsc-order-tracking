from django.test import TestCase

from ..models import Supplier


class TestSupplierManager(TestCase):
    def setUp(self) -> None:
        self.inactive_supplier = Supplier.objects.create(
            name="not active",
            is_active=False,
            website=None,
            has_gravel=True,
            has_pump=True,
            has_concrete=True,
        )

        self.active_supplier = Supplier.objects.create(
            name="active",
            is_active=True,
            website=None,
            has_gravel=True,
            has_pump=True,
            has_concrete=True,
        )

        self.gravel_only_supplier = Supplier.objects.create(
            name="gravel",
            is_active=True,
            website=None,
            has_gravel=True,
            has_pump=False,
            has_concrete=False,
        )

        self.pump_only_supplier = Supplier.objects.create(
            name="pump",
            is_active=True,
            website=None,
            has_gravel=False,
            has_pump=True,
            has_concrete=False,
        )

        self.concrete_only_supplier = Supplier.objects.create(
            name="concrete",
            is_active=True,
            website=None,
            has_gravel=False,
            has_pump=False,
            has_concrete=True,
        )

        self.item_suppliers = [self.gravel_only_supplier, self.pump_only_supplier, self.concrete_only_supplier]

    def test_active_suppliers_returns_only_active(self):
        for supplier in self.item_suppliers:
            self.assertIn(supplier, Supplier.active_suppliers.all())
        self.assertNotIn(self.inactive_supplier, Supplier.active_suppliers.all())

    def test_gravelsupplier_returns_gravel_supplier_only(self):
        self.assertIn(self.gravel_only_supplier, Supplier.gravel_suppliers.all())
        for supplier in self.item_suppliers[1:]:
            self.assertNotIn(supplier, Supplier.gravel_suppliers.all())

    def test_pumpsupplier_returns_pump_supplier_only(self):
        self.assertIn(self.pump_only_supplier, Supplier.pump_suppliers.all())
        for supplier in self.item_suppliers:
            if not supplier == self.pump_only_supplier:
                self.assertNotIn(supplier, Supplier.pump_suppliers.all())

    def test_concretesupplier_returns_concrete_supplier_only(self):
        self.assertIn(self.concrete_only_supplier, Supplier.concrete_suppliers.all())
        for supplier in self.item_suppliers[:1]:
            self.assertNotIn(supplier, Supplier.concrete_suppliers.all())
