from django.test import TestCase

from ..models import GravelItem, Supplier


class TestSupplierModel(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="test supplier",
            is_active=True,
            website="wwww.test.com",
            has_gravel=True,
            has_pump=True,
            has_concrete=True,
        )

        self.no_site_supplier = Supplier.objects.create(
            name="no website supplier",
            is_active=True,
            has_gravel=True,
            has_pump=True,
            has_concrete=True,
        )

    def test_supplier_is_instance(self):
        self.assertIsInstance(self.supplier, Supplier)

    def test_supplier_str_method(self):
        self.assertTrue(self.supplier.__str__() == self.supplier.name.title())

    def test_get_site_without_website(self):
        self.assertEqual(self.no_site_supplier.get_site(), "none provided")

    def test_get_site_with_website(self):
        self.assertEqual(self.supplier.get_site(), '<a href="wwww.test.com" target="blank">wwww.test.com</a>')


class TestSuppliesManagers(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="test supplier",
            is_active=True,
            website="wwww.test.com",
            has_gravel=True,
            has_pump=True,
            has_concrete=True,
        )

        self.no_site_supplier = Supplier.objects.create(
            name="no website supplier",
            is_active=True,
            has_gravel=True,
            has_pump=True,
            has_concrete=True,
        )

    def test_supplier_in_active_suppliers(self):
        self.assertIn(self.supplier, Supplier.active_suppliers.all())

    def test_supplier_in_gravel_suppliers(self):
        self.assertIn(self.supplier, Supplier.gravel_suppliers.all())

    def test_supplier_in_concrete_suppliers(self):
        self.assertIn(self.supplier, Supplier.concrete_suppliers.all())

    def test_supplier_in_pump_suppliers(self):
        self.assertIn(self.supplier, Supplier.pump_suppliers.all())


class TestGravelItemModel(TestCase):
    def setUp(self):
        self.gitem = GravelItem.objects.create(name="test item")

    def test_gravel_item_is_instance(self):
        self.assertIsInstance(self.gitem, GravelItem)

    def test_gravel_item_str(self):
        self.assertEqual(self.gitem.name.title(), self.gitem.__str__())
