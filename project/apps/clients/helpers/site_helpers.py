from django.utils.html import format_html as fh


def get_lots(lots):
    ll = [x.strip() for x in lots.strip(" ").split(",")]
    return fh("<br>".join(ll))
