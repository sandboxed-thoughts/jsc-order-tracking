from django.core.exceptions import ValidationError
from django.test import TestCase

from ..helpers import GarageChoices, MixChoices, OrderStatusChoices, check_supplier_po


class TestGarageChoices(TestCase):
    def setUp(self):
        pass

    def test_garage_choices_has_choices(self):
        self.assertEqual(GarageChoices.choices, [("None", "None"), ("4'", "4'"), ("8'", "8'"), ("9'", "9'")])

    def test_None_choice(self):
        self.assertEqual(GarageChoices.NONE, "None")

    def test_FT4_choice(self):
        self.assertEqual(GarageChoices.FT4, "4'")

    def test_FT8_choice(self):
        self.assertEqual(GarageChoices.FT8, "8'")

    def test_FT9_choice(self):
        self.assertEqual(GarageChoices.FT9, "9'")


class TestOrderStatusChoices(TestCase):
    def setUp(self):
        pass

    def test_status_choices_has_choices(self):
        self.assertEqual(
            OrderStatusChoices.choices,
            [("pending", "Pending"), ("placed", "Placed"), ("canceled", "Canceled"), ("completed", "Completed")],
        )

    def test_PENDING_choice(self):
        self.assertEqual(OrderStatusChoices.PENDING, "pending")

    def test_PLACED_choice(self):
        self.assertEqual(OrderStatusChoices.PLACED, "placed")

    def test_CANCELED_choice(self):
        self.assertEqual(OrderStatusChoices.CANCELED, "canceled")

    def test_COMPLETED_choice(self):
        self.assertEqual(OrderStatusChoices.COMPLETED, "completed")


class TestCheckSupplierPO(TestCase):
    def setUp(self):
        self.po = None
        self.supplier = None

    def test_check_supplier_po_gets_error_without_po(self):
        self.supplier = "Supplier1"
        with self.assertRaises(ValidationError):
            check_supplier_po(self)

    def test_check_supplier_po_gets_error_without_supplier(self):
        self.po = "1234"
        with self.assertRaises(ValidationError):
            check_supplier_po(self)

    def test_check_supplier_po_passes(self):
        self.supplier = "Supplier1"
        self.po = "1234"
        check_supplier_po(self)


class TestMixChoices(TestCase):
    def setUp(self):
        pass

    def test_mix_choices_has_choices(self):
        self.assertEqual(
            MixChoices.choices, [("rich", "rich"), ("standard", "standard"), ("medium", "medium"), ("lean", "lean")]
        )

    def test_RICH_choice(self):
        self.assertEqual(MixChoices.RICH, "rich")

    def test_MEDIUM_choice(self):
        self.assertEqual(MixChoices.MEDIUM, "medium")

    def test_STANDARD_choice(self):
        self.assertEqual(MixChoices.STANDARD, "standard")

    def test_LEAN_choice(self):
        self.assertEqual(MixChoices.LEAN, "lean")
