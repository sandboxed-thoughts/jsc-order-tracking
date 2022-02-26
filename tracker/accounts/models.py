from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords as HR

from  .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom User model replacing the unique identifier with email
    """
    username = None
    email = models.EmailField(_("email address"), max_length=254, unique=True, blank=False, null=False)
    history = HR()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    
    objects = CustomUserManager()
    
    def __str__(self) -> str:
        return "{0}. {1}".format(self.first_name[0], self.last_name)
    
    