from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from ..models import CustomUser as User


class StandardUserTestCase(TestCase):
    """Test the standard CustomUser (user) model"""

    def setUp(self):
        User.objects.create_user(email="test@test.com", first_name="Test", last_name="User", password="password")
        self.user = User.objects.get(email="test@test.com")

    def test_standard_user_is_not_super(self):
        """Standard users should not be superuser"""
        self.user = User.objects.get(email="test@test.com")

        # User is not superuser or admin by default
        self.assertFalse(self.user.is_superuser)

    def test_standard_user_is_active_and_has_usable_password(self):
        """Standard users should not be superuser"""

        # User is active and has a valid password
        self.assertTrue(self.user.has_usable_password)
        self.assertTrue(self.user.is_active)

    def test_standard_user_has_correct_name(self):

        # full_name returns full name
        self.assertTrue(self.user.get_full_name() == "Test User")

        # short_name returns first name
        self.assertTrue(self.user.first_name == self.user.get_short_name())

        # __str__ returns full name
        self.assertTrue(self.user.__str__() == "{0}. {1}".format(self.user.first_name[0], self.user.last_name).title())

    def test_create_user_raises_error_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, first_name="test", last_name="error", password="password")


class SuperUserTestCase(TestCase):
    """Test the standard CustomUser (user) model"""

    def setUp(self):
        User.objects.create_superuser(
            email="super@test.com", first_name="Super", last_name="User", password="password"
        )
        self.super_user = User.objects.get(email="super@test.com")

    def test_superuser_is_superuser(self):
        """superusers should have is_superuser by default"""
        user = self.super_user
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)

    def test_create_superuser_raises_error_without_extra_fields(self):
        with self.assertRaises(ValueError):
            # not staff
            User.objects.create_superuser(
                email="failing@test.test", first_name="Studded", last_name="User", password="password", is_staff=False
            )
        with self.assertRaises(ValueError):
            # not superuser
            User.objects.create_superuser(
                email="failing@test.test",
                first_name="Studded",
                last_name="User",
                password="password",
                is_superuser=False,
            )


class EditableUserManagerTestCase(TestCase):
    """Test that the EditableUserManager returns only non_superusers"""

    def setUp(self):
        User.objects.create_user(
            email="standard@user.test", first_name="standard", last_name="user", password="password"
        )
        User.objects.create_superuser(
            email="super@test.com", first_name="Super", last_name="User", password="password"
        )
        self.user = User.objects.get(email="standard@user.test")
        self.superuser = User.objects.get(email="super@test.com")

    def test_superuser_not_in_editable_users(self):
        self.assertNotIn(self.superuser, User.editable_objects.all())

    def test_standard_user_in_editable_users(self):
        self.assertIn(self.user, User.editable_objects.all())
