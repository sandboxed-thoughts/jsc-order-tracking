from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from apps.clients.helpers import LotChoices
from apps.core.helpers import get_choices
from apps.suppliers.models import Supplier
from apps.clients.models import Lot
from ..helpers import MixChoices


class BaseConcreteOrderForm(forms.ModelForm):
    """Custom form to handle creation of wall orders"""

    supplier_choices = get_choices(list(Supplier.objects.filter(is_active=True)), "name")

    User = get_user_model()
    po = forms.CharField(
        label="purchase order".title(), max_length=50, required=True, validators=[RegexValidator("[\\S\\w]")]
    )
    # https://simpleisbetterthancomplex.com/tutorial/2019/01/02/how-to-implement-grouped-model-choice-field.html
    lots = forms.ModelMultipleChoiceField(label="lots".title(), queryset=Lot.objects.all())
    supplier = forms.ModelChoiceField(label="supplier".title(), queryset=Supplier.objects.filter(is_active=True))
    dispatcher = forms.ModelChoiceField(label="dispatcher".title(), queryset=User.objects.filter(groups__name="Dispatchers"))
    etotal = forms.IntegerField(label="estimated total".title())
    atotal = forms.IntegerField(label="actual total".title(), required=False)
    qordered = forms.IntegerField(
        label="total ordered".title(),
    )
    mix = forms.ChoiceField(label="mix".title(), choices=MixChoices.choices)
    slump = forms.CharField(label="slump".title())
