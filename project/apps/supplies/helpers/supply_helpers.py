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
        raise ValidationError({"po": ValidationError("please add the supplier's PO to the order")})
