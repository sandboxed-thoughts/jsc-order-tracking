from django.db.utils import IntegrityError
from django.forms import ValidationError
from django.test import TestCase

from apps.accounts.models import CustomUser as User
from apps.clients.models import Client, Site
from apps.supplies.models import GravelItem, Supplier
from model_bakery import baker

from ..helpers import MixChoices
from ..models import GravelOrder, GravelOrderNote, ConcreteOrder, ConcreteType, ConcreteOrderNote


class TestGravelOrderModel(TestCase):
    def setUp(self):
        builder = baker.make(Client)
        site = baker.make(Site)
        gravel_item = baker.make(GravelItem)
        self.go = GravelOrder.objects.create(
            builder=builder,
            site=site,
            lots="1234 First St, 5678 First St, 1234 Some Cir, 5678 Some Cir",
            item=gravel_item,
            bsdt="b/s",
        )

    def test_gravel_order_is_instance(self):
        self.assertIsInstance(self.go, GravelOrder)

    def test_gravel_order_get_lots(self):
        self.assertEqual(self.go.get_lots(), "1234 First St<br>5678 First St<br>1234 Some Cir<br>5678 Some Cir")

    def test_nloads_returns_cannot_compute(self):
        self.assertEqual(self.go.nloads(), "cannot compute")

    def test_nloads_returns_undelivered_quantity(self):
        self.go.rloads = 15
        self.go.dloads = 5
        self.assertEqual(self.go.nloads(), 10)

    def test_order_has_status(self):
        self.assertEqual(self.go.status, "pending")

    def test_str_is_pk(self):
        self.assertEqual(str(self.go.pk), self.go.__str__())

    def test_cannot_add_po_without_supplier(self):
        self.go.po = "123 test"
        self.assertRaises(ValidationError, self.go.clean)

    def test_cannot_add_supplier_without_po(self):
        self.go.supplier = baker.make(Supplier)
        self.assertRaises(ValidationError, self.go.clean)


class TestGravelOrderNote(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.builder = baker.make(Client)
        self.site = baker.make(Site)
        gravel_item = baker.make(GravelItem)
        self.go = GravelOrder.objects.create(
            builder=self.builder,
            site=self.site,
            lots="1234 First St, 5678 First St, 1234 Some Cir, 5678 Some Cir",
            item=gravel_item,
            bsdt="b/s",
        )
        self.go_note = GravelOrderNote.objects.create(
            order=self.go,
            author=self.user,
            note="this is a test note",
        )

    def test_note_is_note(self):
        self.assertIsInstance(self.go_note, GravelOrderNote)

    def test_note_references_order(self):
        self.assertEqual(self.go_note.order, self.go)

    def test_note_references_author(self):
        self.assertEqual(self.go_note.author, self.user)

    def test_note_fails_without_author(self):
        with self.assertRaises(AttributeError):
            self.assertIsInstance(GravelOrderNote.create(order=self.go, note="test"), GravelOrderNote)

    def test_note_fails_without_order(self):
        with self.assertRaises(AttributeError):
            self.assertIsInstance(GravelOrderNote.create(author=self.user, note="Test"), GravelOrderNote)

    def test_note_fails_without_note(self):
        with self.assertRaises(AttributeError):
            self.assertIsInstance(GravelOrderNote.create(author=self.user, order=self.go))


class TestConcreteOrderModel(TestCase):

    def setUp(self):
        self.user = baker.make(User)        
        builder = baker.make(Client)
        site = baker.make(Site)
        ConcreteOrder.objects.create(
            dispatcher=self.user,
            builder=builder,
            site=site,
            lots="1234 First St, 5678 First St, 1234 Some Cir, 5678 Some Cir",
            etotal = 15,
        ).save()
        self.co = ConcreteOrder.objects.first()
    def test_order_is_instance(self):
        self.assertIsInstance(self.co, ConcreteOrder)

    def test_order_saves_without_supplier(self):
        self.co.supplier=None
        self.co.save()
        self.assertIsInstance(self.co, ConcreteOrder)

    def test_order_fails_with_supplier_but_not_po(self):
        self.co.supplier = baker.make(Supplier)
        self.assertRaises(ValidationError, self.co.clean)

    def test_order_fails_with_po_but_not_supplier(self):
        self.co.po = "Test-1234"
        self.assertRaises(ValidationError, self.co.clean)


class TestConcreteTypeModel(TestCase):
    def setUp(self):
        self.user = baker.make(User)        
        self.builder = baker.make(Client)
        self.site = baker.make(Site)
        self.order = baker.make(ConcreteOrder)
        self.ctype = ConcreteType.objects.create(
            order = self.order,
            mix = MixChoices.RICH,
            slump = "S3",
            note = "Test Type Note",
        )

    def test_ctype_is_instance(self):
        self.assertIsInstance(self.ctype, ConcreteType)

    def test_concrete_type_fails_without_order(self):
        with self.assertRaises(IntegrityError):
            self.assertIsInstance(
                ConcreteType.objects.create(
                    mix=MixChoices.LEAN,
                    slump = "S2",
                ),
                ConcreteType
            )