from django.utils.html import format_html as fh


def get_addr(self) -> str:
    if any([self.street, self.city, self.state, self.zipcode]):
        address = "<address>"
        if self.street is not None:
            address += "{}<br>".format(self.street)
        if self.city is not None:
            address += "{}, ".format(self.city)
        if self.state is not None:
            address += "{} ".format(self.state)
        if self.zipcode is not None:
            address += self.zipcode
        address += "</address>"
        return fh(address)
    return "not provided"


def get_untagged_addr(self) -> str:
    address = ""
    if self.street is not None:
        address += "{}, ".format(self.street)
    if self.city is not None:
        address += "{}, ".format(self.city)
    if self.state is not None:
        address += "{} ".format(self.state)
    if self.zipcode is not None:
        address += "{}".format(self.zipcode)
    return address


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
