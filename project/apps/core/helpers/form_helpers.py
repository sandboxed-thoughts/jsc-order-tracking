from functools import partial
from itertools import groupby
from operator import attrgetter

from django.forms.models import ModelChoiceField, ModelChoiceIterator, ModelMultipleChoiceField


def get_choice_list(choice_items) -> list:

    choices = ()
    for k, v in choice_items.items():
        choices += (
            (
                k,
                (v),
            ),
        )
    return choices


def get_choices(model, label_field, category_field=None):
    choice_dict = {}
    for inst in model:
        print(inst.__class__())
        inst_label = (inst.pk, getattr(inst, label_field).title())
        if category_field in choice_dict.keys():
            choice_dict[category_field] += ((inst_label),)
        else:
            choice_dict[category_field] = ((inst_label),)

    choices = get_choice_list(choice_dict)

    return choices


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __init__(self, field, groupby):
        self.groupby = groupby
        super().__init__(field)

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset
        # Can't use iterator() when queryset uses prefetch_related()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, objs in groupby(queryset, self.groupby):
            yield (group, [self.choice(obj) for obj in objs])


class GroupedModelChoiceField(ModelChoiceField):
    def __init__(self, *args, choices_groupby, **kwargs):
        if isinstance(choices_groupby, str):
            choices_groupby = attrgetter(choices_groupby)
        elif not callable(choices_groupby):
            raise TypeError("choices_groupby must either be a str or a callable accepting a single argument")
        self.iterator = partial(GroupedModelChoiceIterator, groupby=choices_groupby)
        super().__init__(*args, **kwargs)


class GroupedModelMultipleChoiceField(GroupedModelChoiceField):
    pass
