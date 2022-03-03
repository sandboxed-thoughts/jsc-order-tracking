from django.test import TestCase
from .models import CustomUser as CU


class CustomUserTest(TestCase):
    def setUp(self):
        self.su = CU.objects.create_superuser(
            email="superuser@test.case", password="password", first_name="Super", last_name="User"
        )
        self.stdu = CU.objects.create_user(
            email="standarduser@test.case", password="password", first_name="Standard", last_name="User"
        )

    def test_create_user(self):
        """Test the creation of a standard CustomUser"""
        user = self.stdu
        self.assertTrue(isinstance(user, CU))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.get_full_name(), "Standard User")

    def test_create_supeeruser(self):
        """Test the creation of a super CustomUser"""
        su = self.su
        self.assertTrue(isinstance(su, CU))
        self.assertTrue(su.is_active)
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_superuser)
        self.assertTrue(su.get_full_name(), "Super User")
