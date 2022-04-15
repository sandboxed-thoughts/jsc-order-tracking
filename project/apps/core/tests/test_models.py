from django.test import TestCase

from ..models import get_addr, get_untagged_addr


class TestAddrHelpers(TestCase):
    def setUp(self):
        class Addr:
            def __init__(self, street=None, city=None, state=None, zipcode=None, *args, **kwargs):
                self.street = street
                self.city = city
                self.state = state
                self.zipcode = zipcode

        self.full_address = Addr(street=" 23 Test St", city="Test City", state="VA", zipcode="12345")

        self.no_st = Addr(city="Test City", state="VA", zipcode="12345")

        self.state_only = Addr(state="Virginia")

        self.no_addr = Addr()

    def test_get_addr(self):
        address = self.full_address
        correct_fmt = "<address>{0}<br>{1}, {2} {3}</address>".format(
            address.street, address.city, address.state, address.zipcode
        )

        self.assertEqual(get_addr(address), correct_fmt)

    def test_get_untagged_addr(self):
        address = self.full_address
        correct_fmt = "{0}, {1}, {2} {3}".format(address.street, address.city, address.state, address.zipcode)

        self.assertEqual(get_untagged_addr(address), correct_fmt)

    def test_address_without_street(self):
        address = self.no_st
        correct_tagged = "<address>{0}, {1} {2}</address>".format(address.city, address.state, address.zipcode)
        correct_untagged = "{0}, {1} {2}".format(address.city, address.state, address.zipcode)

        self.assertEqual(get_addr(address), correct_tagged)
        self.assertEqual(get_untagged_addr(address), correct_untagged)

    def test_address_with_only_state(self):
        address = self.state_only
        self.assertEqual(get_addr(address), "<address>Virginia </address>")
        self.assertEqual(get_untagged_addr(address), "Virginia ")

    def test_no_address(self):
        address = self.no_addr

        self.assertEqual(get_addr(address), "not provided")
        self.assertEqual(get_untagged_addr(address), "")
