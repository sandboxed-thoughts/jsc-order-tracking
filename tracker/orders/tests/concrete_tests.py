from django.test import TestCase
from orders.models import Concrete

class ConcreteTest(TestCase):
    """Test the Concrete model from Orders"""
    
    def setUp(self):
        self.corder = Concrete.objects.create(
            bldr="James",
            job_site="Coldwell St.",
            lot = "10114, 10115",
            item = "concrete",
            supplier = "Concrete 'R Us",
            dsph = "Terry",
            ono = 45587,
            etot = 50,
            qord = 55,
            ctype='mix',
        )
        
    def test_concrete_model(self):
        self.assertTrue(isinstance(self.corder, Concrete))
        self.assertEqual(self.corder.get_lots(), '10114<br> 10115')
        