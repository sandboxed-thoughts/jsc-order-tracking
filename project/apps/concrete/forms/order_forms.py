from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator


from ..helpers import MixChoices
from apps.clients.helpers import LotChoices
from apps.suppliers.models import Supplier
from apps.core.helpers import get_choices
class BaseConcreteOrderForm(forms.ModelForm):
    """Custom form to handle creation of wall orders
    
    """

    supplier_choices = get_choices(Supplier.objects.filter(is_active=True), "name")

    user = get_user_model()
    po = forms.CharField(label="purchase order".title(), max_length=50, required=True,validators=[RegexValidator("[\\S\\w]")])
    lots = forms.MultipleChoiceField(label='lots'.title(), choices=LotChoices.choices)
    supplier = forms.ChoiceField(label="supplier".title(), choices=supplier_choices)
    dispatcher = forms.ChoiceField(label="dispatcher".title(), choices=user.objects.filter(groups__name='dispatchers'))
    etotal = forms.IntegerField(label="estimated total".title())
    atotal = forms.IntegerField(label='actual total'.title(), required=False)
    qordered = forms.IntegerField(label="total ordered".title(),)
    mix = forms.ChoiceField(label='mix'.title(), choices=MixChoices.choices)
    slump = forms.CharField(label="slump".title())
    