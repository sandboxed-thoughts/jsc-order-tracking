from django.forms import ValidationError
from django.test import TestCase
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from model_bakery import baker

from ..models import GravelDeliverySchedule


class TestGravelDeliverySchedule(TestCase):
    def setUp(self):
        self.driver = baker.make("accounts.CustomUser")
        self.supplier = baker.make("supplies.Supplier")
        self.order = baker.make("orders.GravelOrder", supplier=self.supplier, po=123456678)
        self.supplier_delivers_order = baker.make("orders.GravelOrder", supplier=self.supplier, po=12345566)
        self.complete_order = baker.make("orders.Gravelorder", rloads=10, dloads=10)
        self.driver_delivery = baker.make(
            GravelDeliverySchedule, driver=baker.make("accounts.CustomUser"), order=self.order
        )
        self.supplier_delivery = baker.make(
            GravelDeliverySchedule,
            supplier_delivers=True,
            driver=None,
            order=self.supplier_delivers_order,
        )

    def test_get_driver_for_supplier_delivers(self):
        self.assertEqual(self.supplier_delivery.get_driver(), self.order.supplier.name.title())

    def test_get_driver_for_driver(self):
        self.assertEqual(self.driver_delivery.get_driver(), self.driver_delivery.driver.get_full_name())

    def test_get_str_method(self):
        self.assertEqual(
            self.driver_delivery.__str__(),
            "{0} [{1}]".format(self.driver_delivery.driver.get_full_name(), self.driver_delivery.pk),
        )

    def test_only_one_driver_can_be_assigned(self):
        with self.assertRaises(ValidationError):
            baker.make(
                GravelDeliverySchedule,
                driver=self.driver,
                supplier_delivers=True,
                order=self.order,
            ).clean()

    def test_one_driver_needs_to_be_assigned(self):
        with self.assertRaises(ValidationError):
            baker.make(
                GravelDeliverySchedule,
                driver=None,
                supplier_delivers=False,
                order=self.order,
            ).clean()
