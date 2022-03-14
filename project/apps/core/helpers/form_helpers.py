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
    print(choice_dict)

    choices = get_choice_list(choice_dict)

    return choices
