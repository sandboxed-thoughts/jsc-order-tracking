from django.test import TestCase
from django.urls import NoReverseMatch

from model_bakery import baker

from ..models import Client


class TestBuilderModel(TestCase):
    def setUp(self):
        self.client = baker.make(Client)

    def test_client_is_active(self):
        self.assertTrue(self.client.is_active)

    def test_client_has_str(self):
        self.assertEqual(self.client.__str__(), self.client.name.title())

    def test_client_has_slug(self):
        self.assertIsNotNone(self.client.slug)
