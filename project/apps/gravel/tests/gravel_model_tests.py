from django.test import TestCase

from ..models import StoneType


class TestStoneTypeModel(TestCase):
    def setUp(self):
        self.stone = StoneType.objects.create(name="test stone", description="this is a stone designed for testing purposes")

    def test_stonetype_model_creation(self):
        self.assertIsInstance(self.stone, StoneType)
        self.assertTrue(self.stone.__str__() == self.stone.name.title())
