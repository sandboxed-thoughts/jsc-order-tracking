from django.test import TestCase

from model_bakery import baker

from ..models import Client


class TestActiveBuilderManager(TestCase):
    def setUp(self):
        self.active_client = baker.make(Client)
        self.inactive_client = baker.make(Client, is_active=False)

    def test_active_client_in_manager(self):
        self.assertIn(self.active_client, Client.active_clients.all())

    def test_inactive_client_not_in_manager(self):
        self.assertNotIn(self.inactive_client, Client.active_clients.all())
