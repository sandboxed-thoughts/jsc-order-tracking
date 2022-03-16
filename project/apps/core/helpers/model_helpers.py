from django.utils.html import format_html as fh


def get_addr(self) -> str:
    if self.street is None:
        parts = [self.city, self.state, self.zipcode]
    else:
        parts = [self.street, "<br>", self.city, self.state, self.zipcode]
    if any(parts):
        count = len(parts) - 1
        address = "<address>"
        for k, v in enumerate(parts):
            if v is not None:
                address += v.title()
            if v == self.city and self.city is not None:
                address += ", "
            elif 2 <= k < count:
                address += " "
        address += "</address>"
        return fh(address)
    return "not provided"
