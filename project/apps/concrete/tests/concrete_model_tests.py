from django.test import TestCase

from model_bakery import baker

from ..models import ConcreteType


class TestConcreteModel(TestCase):
    def setUp(self):
        self.model = baker.make(ConcreteType)

    def test_model_is_instance(self):
        self.assertIsInstance(self.model, ConcreteType)

    def test_str_is_valid(self):
        self.assertEqual(self.model.__str__(), "{0}/{1}".format(self.model.mix, self.model.slump))
