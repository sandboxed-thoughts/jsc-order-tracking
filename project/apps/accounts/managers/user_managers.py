from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    """

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a User with the given email, first_name, last_name, and password
        """

        # validation
        if not email:
            raise ValueError(_("The user must have an email address"))
        if not first_name or not last_name:
            raise ValueError(_("The user must have a full name"))
        if not password:
            raise ValueError(_("Tue user must have a password"))

        # fields
        email = self.normalize_email(email).lower()
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        first_name = first_name.lower()
        last_name = last_name.lower()
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email, first_name, last_name, and password
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superusers must be staff"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superusers must be superusers"))
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class EditableUserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=False)
