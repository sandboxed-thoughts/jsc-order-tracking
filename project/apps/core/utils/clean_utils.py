from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def check_supplier_po(self):
    if self.po and not self.supplier:
        raise ValidationError(
            {
                "supplier": ValidationError("please add the PO's supplier to the order"),
            }
        )

    if self.supplier and not self.po:
        raise ValidationError(
            {
                "po": ValidationError("please add the supplier's PO to the order")
            }
        )


def check_delivery_driver(self):
    """
    Require at least one of supplier_delivers or driver to be set - but not both
    """
    if not (self.supplier_delivers or self.driver):
        raise ValidationError(
            {
                "supplier_delivers": ValidationError(_("Someone must deliver the order.")),
                "driver": ValidationError(_("Someone must deliver the order.")),
            }
        )
    if self.supplier_delivers and self.driver:
        raise ValidationError(
            {
                "supplier_delivers": ValidationError(
                    _("only one can deliver, please remove one of these options")
                ),
                "driver": ValidationError(_("only one can deliver, please remove one of these options")),
            }
        )
