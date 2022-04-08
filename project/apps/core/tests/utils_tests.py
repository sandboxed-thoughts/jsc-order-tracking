from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError

from django.test import TestCase

from apps.accounts.models import CustomUser as User

from ..utils import check_supplier_po, group_check


class TestViewHelpers(TestCase):
    def setUp(self):
        User.objects.create_superuser(
            email="test@super.local", first_name="super", last_name="user", password="password"
        )
        self.user = User.objects.get(email="test@super.local")

    def test_group_check(self):
        self.assertTrue(group_check(self.user, ["Admin"]))
        self.assertFalse(group_check(AnonymousUser, ["Admin"]))


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
