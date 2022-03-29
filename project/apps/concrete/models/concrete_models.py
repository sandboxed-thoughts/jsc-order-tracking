from django.db import models
from django.utils.translation import gettext_lazy as _

from ..helpers import MixChoices


class ConcreteType(models.Model):
    """Various orderable types of concrete"""

    order = models.ForeignKey("orders.ConcreteOrder", verbose_name=_("concrete orders"), on_delete=models.CASCADE)
    mix = models.CharField(_("mix"), max_length=10, choices=MixChoices.choices, default=MixChoices.STANDARD)
    slump = models.CharField(_("slump"), max_length=6)
    note = models.TextField(_("note"), blank=True, null=True, max_length=250)

    def __str__(self):
        return "{0}/{1}".format(self.mix, self.slump)

    class Meta:
        db_table = "concrete_types"
        managed = True
        verbose_name = "Concrete Type"
        verbose_name_plural = "Concrete Types"
