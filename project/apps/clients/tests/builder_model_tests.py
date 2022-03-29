from django.test import TestCase
from django.urls import NoReverseMatch

from model_bakery import baker

from ..models import BuilderModel as Builder


class TestBuilderModel(TestCase):
    def setUp(self):
        self.builder = baker.make(Builder)

    def test_builder_is_active(self):
        self.assertTrue(self.builder.is_active)

    def test_builder_has_str(self):
        self.assertEqual(self.builder.__str__(), self.builder.name.title())

    def test_builder_has_slug(self):
        self.assertIsNotNone(self.builder.slug)

    def test_absolute_url(self):
        with self.assertRaises(NoReverseMatch):  # called because there is no url set for the app
            self.assertEqual(self.builder.get_absolute_url(), "/builders/view/{}".format(self.slug))
