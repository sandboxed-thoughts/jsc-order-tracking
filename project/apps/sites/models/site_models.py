from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.models import AddressModel, NoteModel
from simple_history.models import HistoricalRecords as HR

User = settings.AUTH_USER_MODEL


class SiteModel(AddressModel):
    """
    Customer worksites

    Fields:
        site_name:  CharField,
        street:     None,
        city:       CharField,
        state:      localflavor.us.models.USStateField,
        zipcode:    localflavor.us.models.USZipCodeField,
        project_manager:    CustomUser.get_pms

    Methods:
        get_addr:   returns the instance's full formatted address as html,
    """

    class Meta:
        db_table = "sites_subdivisions"
        managed = True
        verbose_name = "Subdivision"
        verbose_name_plural = "Subdivisions"

    street = None
    site_name = models.CharField(_("Site Name"), max_length=100)
    is_active = models.BooleanField(_("Active"), default=True)
    slug = models.SlugField(_("url"), blank=True, max_length=100)
    created_on = models.DateTimeField(_("created on"), auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(_("last updated"), auto_now=True, auto_now_add=False)
    project_manager = models.ForeignKey(
        User,
        verbose_name=_("project manager"),
        related_name="pm_pump_schedules",
        limit_choices_to={"groups__name": "Project Managers"},
        on_delete=models.CASCADE,
    )

    history = HR()

    def __str__(self):
        return self.site_name

    def get_absolute_url(self):
        return reverse("site_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.site_name)
        super(SiteModel, self).save(*args, **kwargs)  # Call the real save() method


class SiteNote(NoteModel):
    site = models.ForeignKey(SiteModel, verbose_name=_("site note"), on_delete=models.CASCADE)
