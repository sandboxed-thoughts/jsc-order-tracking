from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.accounts.models import CustomUser as User

from ..views import group_check


class TestViewHelpers(TestCase):
    def setUp(self):
        User.objects.create_superuser(
            email="test@super.local", first_name="super", last_name="user", password="password"
        )
        self.user = User.objects.get(email="test@super.local")

    def test_group_check(self):
        self.assertTrue(group_check(self.user, ["Admin"]))
        self.assertFalse(group_check(AnonymousUser, ["Admin"]))
