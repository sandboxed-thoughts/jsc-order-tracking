from django.conf import settings
from django.contrib import admin
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.admin import get_notes
from apps.core.models import AddressModel, NoteModel
from simple_history.models import HistoricalRecords as HR

User = settings.AUTH_USER_MODEL


class Site(AddressModel):
    """
    Customer worksites

    Args:
        name            (str):          CharField
        street          (str):          None
        city            (str):          CharField
        state           (str):          localflavor.us.models.USStateField
        zipcode         (str):          localflavor.us.models.USZipCodeField
        project_manager (int):          ForeignKey -> CustomUser.get_pms

        get_addr(self) -> str:   returns the instance's full formatted address as html
    """

    class Meta:
        db_table = "clients_sites"
        managed = True
        verbose_name = "Subdivision"
        verbose_name_plural = "Subdivisions"

    street = None
    name = models.CharField(_("subdivision name"), max_length=100)
    is_active = models.BooleanField(_("active"), default=True)
    slug = models.SlugField(_("url"), blank=True, max_length=100)
    created_on = models.DateTimeField(_("created on"), auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(_("last updated"), auto_now=True, auto_now_add=False)
    project_manager = models.ForeignKey(
        User,
        verbose_name=_("project manager"),
        related_name="pm_sites",
        limit_choices_to={"groups__name": "Project Managers"},
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    history = HR()

    def __str__(self):
        return self.name

    @admin.display(description="", empty_value="")
    def get_notes(self):
        return get_notes(self.site_notes.all())

    def get_absolute_url(self):
        return reverse("site_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Site, self).save(*args, **kwargs)  # Call the real save() method


class SiteNote(NoteModel):
    site = models.ForeignKey(Site, verbose_name=_("site note"), related_name="site_notes", on_delete=models.CASCADE)
