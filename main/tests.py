from django.test import TestCase
from .models.user import Customers

# Create your tests here.
class MainTestApp(TestCase):
	def test_customer(self):
		customer = Customers.objects.create(
			name = 'Testing',
			email = 'Testing@testing.com',
			birth_date = '17/02/1999',
			phone = '+62857126'
		)
		self.assertEqual(customer.name, "Testing")
		self.assertEqual(customer.email, "Testing@testing.com")
		self.assertEqual(customer.birth_date, "17/02/1999")
		self.assertEqual(customer.phone, "+62857126")