from django.test import TestCase

from model_bakery import baker

from ..models import Site


class TestSiteModel(TestCase):
    def setUp(self):
        self.site = baker.make(Site)

    def test_site_is_active(self):
        self.assertTrue(self.site.is_active)

    def test_site_has_str(self):
        self.assertEqual(self.site.name, self.site.__str__())
