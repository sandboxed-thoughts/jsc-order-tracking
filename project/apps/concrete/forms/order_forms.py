from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from apps.clients.models import Lot
from apps.core.helpers import GroupedModelMultipleChoiceField, get_choices
from apps.suppliers.models import Supplier

from ..helpers import MixChoices


class BaseConcreteOrderForm(forms.ModelForm):
    """Custom form to handle creation of wall orders

    This form will cover every field found in all three types of concrete orders (flatwork, foundation, and walls) including the one-to-one PumpInfo


   Thanks to Simple is Better Than Complex : https://rb.gy/t5diij
   
    """

    # user model

    User = get_user_model()

    # fields

    po = forms.CharField(
        label="purchase order".title(), max_length=50, required=True, validators=[RegexValidator("[\\S\\w]")]
    )
    lots = GroupedModelMultipleChoiceField(
        label="lots".title(), queryset=Lot.objects.all(), choices_groupby="subdivision.name"
    )
    supplier = forms.ModelChoiceField(label="supplier".title(), queryset=Supplier.objects.filter(is_active=True))
    dispatcher = forms.ModelChoiceField(
        label="dispatcher".title(), queryset=User.objects.filter(groups__name="Dispatchers")
    )
    etotal = forms.IntegerField(label="estimated total".title())
    atotal = forms.IntegerField(label="actual total".title(), required=False)
    qordered = forms.IntegerField(
        label="total ordered".title(),
    )
    mix = forms.ChoiceField(label="mix".title(), choices=MixChoices.choices)
    slump = forms.CharField(label="slump".title())
    # pump info
    crew = forms.ModelChoiceField(
        label="dispatcher".title(), queryset=User.objects.filter(groups__name="Operators")
    )