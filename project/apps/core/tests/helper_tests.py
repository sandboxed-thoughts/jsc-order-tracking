from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from apps.accounts.models import CustomUser as User

from ..helpers import get_addr, get_choice_list, get_choices, get_untagged_addr
from ..utils import group_check


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


class TestViewHelpers(TestCase):
    def setUp(self):
        User.objects.create_superuser(
            email="test@super.local", first_name="super", last_name="user", password="password"
        )
        self.user = User.objects.get(email="test@super.local")

    def test_group_check(self):
        self.assertTrue(group_check(self.user, ["Admin"]))
        self.assertFalse(group_check(AnonymousUser, ["Admin"]))


class TestFormHelpers(TestCase):
    def setUp(self):
        self.choice_items = {"states": ["Virginia", "Maryland"], "state_abbrs": ["VA", "MD"]}

    def test_get_choice_list(self):
        choice_fmt = (("states", ["Virginia", "Maryland"]), ("state_abbrs", ["VA", "MD"]))
        self.assertEqual(get_choice_list(self.choice_items), choice_fmt)
