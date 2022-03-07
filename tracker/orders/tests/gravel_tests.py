import datetime

from django.test import TestCase

from orders.models import Gravel


class GravelOrderTest(TestCase):
    """Test the creation of a Gravel order"""

    def setUp(self):
        self.gorder = Gravel.objects.create(
            bldr="Driveways 'R Us",
            job_site="Terrywell",
            lot=1698,
            caller="James",
            r_loads=15,
            stone="Crush",
            supplier="Construction Supplies",
            n_date=datetime.date(2022, 3, 28),
            priority="High",
            po=1348875,
        )

    def test_gravel_order(self):
        order = self.gorder
        self.assertTrue(isinstance(order, Gravel))
