from django.test import TestCase

from model_bakery import baker

from ..models import BuilderModel as Builder


class TestActiveBuilderManager(TestCase):
    def setUp(self):
        self.active_builder = baker.make(Builder)
        self.inactive_builder = baker.make(Builder, is_active=False)

    def test_active_builder_in_manager(self):
        self.assertIn(self.active_builder, Builder.active_builders.all())

    def test_inactive_builder_not_in_manager(self):
        self.assertNotIn(self.inactive_builder, Builder.active_builders.all())
