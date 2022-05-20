from django.core.exceptions import ValidationError
from django.db.models import TextChoices
from django.utils import timezone
from django.utils.html import format_html as fh
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


def get_po():
    t = timezone.localtime().now()
    tl = [t.year, t.month, t.day, t.hour, t.minute, t.second]
    return int("".join([str(i) for i in tl]))


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
