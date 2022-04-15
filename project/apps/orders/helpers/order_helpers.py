from django.db.models import TextChoices
from django.utils.html import format_html as fh


def format_lots(self):
    """Formats the string of comma-separated lots into a block of lots
    separated by the html tag "<br>"

    Returns:
        str: lots stripped of whitespace and rejoined by <br> tags

    Example:
        str: "1234 example st, 5678 example cir"
        returns: "1234 example st<br>5678 example cir"
    """
    ll = [x.strip() for x in self.lots.strip(" ").split(",")]
    pll = "<br>".join(ll)
    return fh(pll)


from django.core.exceptions import ValidationError
from django.db.models import TextChoices
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


class OrderStatusChoices(TextChoices):
    PENDING = "pending", "Pending"
    PLACED = "placed", "Placed"
    CANCELED = "canceled", "Canceled"
    COMPLETED = "completed", "Completed"


class GarageChoices(TextChoices):
    NONE = None, "None"
    FT4 = "4'", "4'"
    FT8 = "8'", "8'"
    FT9 = "9'", "9'"


class MixChoices(TextChoices):
    RICH = "rich", "rich"
    STANDARD = "standard", "standard"
    MEDIUM = "medium", "medium"
    LEAN = "lean", "lean"