from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from model_bakery import baker

from ..models import CustomUser as User


class TestCustomUserManager(TestCase):
    """Test the default CustomUser manager"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@manager.test", first_name="std", last_name="manager", password="password"
        )
        self.superuser = User.objects.create_superuser(
            email="super@test.com", first_name="Super", last_name="User", password="password"
        )

    def test_create_user_has_usable_password(self):
        self.assertTrue(self.user.has_usable_password())

    def test_create_user_raises_error_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, first_name="test", last_name="error", password="password")

    def test_create_user_raises_error_without_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="std@test.user", first_name="test", last_name="error", password=None)

    def test_create_user_raises_error_without_name(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="std@test.user", first_name=None, last_name="error", password="password")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="std@test.user", first_name="error", last_name=None, password="password")

    def test_create_user_is_not_superuser(self):
        self.assertFalse(self.user.is_superuser)

    def test_create_user_is_staff(self):
        self.assertTrue(self.user.is_staff)

    def test_create_user_is_active(self):
        self.assertTrue(self.user.is_active)

    def test_create_superuser_is_superuser(self):
        self.assertTrue(self.superuser.is_superuser)

    def test_create_superuser_is_staff(self):
        self.assertTrue(self.superuser.is_staff)

    def test_create_superuser_is_active(self):
        self.assertTrue(self.superuser.is_active)

    def test_create_superuser_raises_error_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=None, first_name="test", last_name="error", password="password")

    def test_create_superuser_raises_error_without_is_staff(self):
        with self.assertRaises(ValueError):
            # not staff
            User.objects.create_superuser(
                email="failing@test.test", first_name="Studded", last_name="User", password="password", is_staff=False
            )

    def test_create_superuser_raises_error_without_is_superuser(self):
        with self.assertRaises(ValueError):
            # not superuser
            User.objects.create_superuser(
                email="failing@test.test",
                first_name="Studded",
                last_name="User",
                password="password",
                is_superuser=False,
            )


class TestEditableUserManager(TestCase):
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


class StandardUserTestCase(TestCase):
    """Test the standard CustomUser (user) model"""

    def setUp(self):
        user = baker.make(User, email="test@test.test", first_name="test", last_name="user")
        self.user = user

    def test_standard_user_exists(self):
        """Standard Users should be an instance of CustomUser"""
        self.assertIsInstance(self.user, User)

    def test_standard_user_is_not_super(self):
        """Standard users should not be superuser"""
        self.assertFalse(self.user.is_superuser)

    def test_standard_user_is_active(self):
        """Standard users should be active"""
        self.assertTrue(self.user.is_active)

    def test_standard_user_has_usable_password(self):
        """Standard users should have a usable password"""
        self.assertTrue(self.user.has_usable_password)

    def test_standard_user_has_correct_name(self):

        # user has first_name
        self.assertTrue(self.user.first_name is not None)

        # user has last_name
        self.assertTrue(self.user.last_name is not None)

        # full_name returns full name
        self.assertTrue(self.user.get_full_name() == "Test User")

        # __str__ returns full name
        self.assertTrue(self.user.__str__() == "T. User")


class SuperUserTestCase(TestCase):
    """Test the standard CustomUser (user) model"""

    def setUp(self):
        self.super_user = baker.make(
            User,
            email="super@test.test",
            first_name="Super",
            last_name="User",
            password="password",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

    def test_superuser_is_superuser(self):
        """superusers should have is_superuser by default"""
        user = self.super_user
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
