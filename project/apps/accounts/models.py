from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager, EditableUserManager


class CustomUser(AbstractUser):
    """
    Custom User model replacing the unique identifier with email
    """

    username = None
    email = models.EmailField(_("email address"), max_length=254, unique=True, blank=False, null=False)
    is_staff = models.BooleanField(_("staff status"), default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()
    editable_objects = EditableUserManager()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip().title()

    def __str__(self) -> str:
        return "{0}. {1}".format(self.first_name[0], self.last_name).title()

    def save(self, *args, **kwargs):
        # if CustomUser.objects.get(email=self.email):

        return super(CustomUser, self).save()
