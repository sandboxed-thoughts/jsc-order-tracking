from django.utils.html import format_html as fh


def get_lots(lots):
    ll = [x for x in lots.strip(" ").split(",")]
    pll = "<br>".join(ll)
    return fh(pll)
