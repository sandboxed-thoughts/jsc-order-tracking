from django.test import TestCase

from ..forms import get_choice_list, get_choices


class TestFormHelpers(TestCase):
    def setUp(self):
        self.choice_items = {"states": ["Virginia", "Maryland"], "state_abbrs": ["VA", "MD"]}

    def test_get_choice_list(self):
        choice_fmt = (("states", ["Virginia", "Maryland"]), ("state_abbrs", ["VA", "MD"]))
        self.assertEqual(get_choice_list(self.choice_items), choice_fmt)
