from apps.core.helpers.form_helpers import get_choice_list
from .models import Lot
from apps.core.helpers import get_choice_list



class LotChoices:
    """Returns a list of lots suited for a choice field"""
    
    def choices():
        lots = Lot.objects.all()
        kwargs = {}
        for lot in lots:
            lot_id = lot.subdivision.name.title()
            lot_select = (lot.pk, "{} ({})".format(lot.name.title(), lot.builder.name.title()))
            if lot_id in kwargs.keys():
                kwargs[lot_id] += ((lot_select),)
            else:
                kwargs[lot_id] = ((lot_select),)
        

        choices = get_choice_list(kwargs)
        return choices

