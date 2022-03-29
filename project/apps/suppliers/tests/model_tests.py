from django.test import TestCase

from model_bakery import baker

from ..models import Supplier


class TestSupplierModel(TestCase):
    def setUp(self):
        self.supplier = baker.make(Supplier)
        self.ws_supplier = baker.make(Supplier, website="www.google.com")

    def test_supplier_is_instance(self):
        self.assertIsInstance(self.supplier, Supplier)

    def test_supplier_str_method(self):
        self.assertTrue(self.supplier.__str__() == self.supplier.name.title())

    def test_get_site_without_website(self):
        self.assertEqual(self.supplier.get_site(), "none provided")

    def test_get_site_with_website(self):
        self.assertEqual(self.ws_supplier.get_site(), '<a href="www.google.com" target="blank">www.google.com</a>')
