from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.models import CommunicationsModel
from simple_history.models import HistoricalRecords as HR

from ..managers import ActiveClientManager


class Client(CommunicationsModel):
    """Django model for clients

    Args:
        CommunicationsModel (model):        email, phone, fax, address
        name                (str):          CharField
        is_active           (bool):         CharField
        date_created        (datetime):     CharField
        date_updated        (datetime):     CharField
        slug                (str):          CharField

    Manangers:
        objects             (queryset):     all instances of Client
        active_builders     (queryset):     all instances of Client where is_active = True

    Methods:
        __str__             (str):          name.title()
        get_absolute_url    (str):          /clients/view/slug
        save                (object):       saved instance with auto-populated slug field from slugifying name
    """

    class Meta:
        db_table = "clients"
        managed = True
        verbose_name = _("Builder")
        verbose_name_plural = _("Builders")

    name = models.CharField(_("builder name"), max_length=150, unique=True)
    is_active = models.BooleanField(
        _("active builder"),
        default=True,
    )
    date_created = models.DateTimeField(_("created on"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(_("updated on"), auto_now=True, auto_now_add=False)
    slug = models.SlugField(max_length=150, blank=True)

    history = HR()

    objects = models.Manager()
    active_clients = ActiveClientManager()

    def __str__(self) -> str:
        return self.name.title()

    def get_absolute_url(self):
        return reverse("clients:view", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Client, self).save(*args, **kwargs)  # Call the real save() method
