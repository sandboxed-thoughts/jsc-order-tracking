from django.test import TestCase

from ..helpers import MixChoices


class TestMixChoices(TestCase):
    def setUp(self):
        self.rich = MixChoices.RICH
        self.std = MixChoices.STANDARD
        self.med = MixChoices.MEDIUM
        self.lean = MixChoices.LEAN

    def test_RICH_is_rich(self):
        self.assertEqual(self.rich, "rich")
        self.assertIn((self.rich, "rich"), MixChoices.choices)

    def test_STANDARD_is_standard(self):
        self.assertEqual(self.std, "standard")
        self.assertIn((self.std, "standard"), MixChoices.choices)

    def test_MEDIUM_is_medium(self):
        self.assertEqual(self.med, "medium")
        self.assertIn((self.med, "medium"), MixChoices.choices)

    def test_LEAN_is_lean(self):
        self.assertEqual(self.lean, "lean")
        self.assertIn((self.lean, "lean"), MixChoices.choices)
