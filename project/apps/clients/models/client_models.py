from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.models import CommunicationsModel
from simple_history.models import HistoricalRecords as HR

from ..managers import ActiveBuilderManager


class BuilderModel(CommunicationsModel):
    class Meta:
        db_table = "clients_builders"
        managed = True
        verbose_name = "Builder"
        verbose_name_plural = "Builders"

    name = models.CharField(_("name"), max_length=150, unique=True)
    is_active = models.BooleanField(
        _("active builder"),
        default=True,
    )
    date_created = models.DateTimeField(_("created on"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(_("updated on"), auto_now=True, auto_now_add=False)
    slug = models.SlugField(max_length=50, blank=True)

    history = HR()

    objects = models.Manager()
    active_builders = ActiveBuilderManager()

    def __str__(self) -> str:
        return self.name.title()

    def get_absolute_url(self):
        return reverse("clients:view", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(BuilderModel, self).save(*args, **kwargs)  # Call the real save() method
