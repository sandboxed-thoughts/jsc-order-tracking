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
