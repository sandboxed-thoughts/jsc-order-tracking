from django.test import TestCase

from ..models import BuilderModel as Builder


class BuilderTest(TestCase):
    def setUp(self):
        Builder.objects.create(name="The Builder")
        self.builder = Builder.objects.get(name="The Builder")

    def test_builder_is_active(self):
        self.assertIn(self.builder, Builder.active_builders.all())
        self.assertTrue(self.builder.is_active)

    def test_builder_has_str(self):
        self.assertEqual(self.builder.__str__(), "The Builder")

    def test_builder_has_slug(self):
        self.assertTrue(self.builder.slug is not None)
