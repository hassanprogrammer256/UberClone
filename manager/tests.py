from datetime import date, time
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from accounts.models import CustomerProfile
from api.models import CustomerPayment


class CustomersViewTests(TestCase):
	def setUp(self):
		self.user_model = get_user_model()
		self.admin = self.user_model.objects.create_user(
			phone_number='+256700000001',
			email='admin@example.com',
			password='test-password',
			role='admin',
		)
		self.client.force_login(self.admin)
		self.url = reverse('admin_customers')

	def test_customer_directory_renders_gender_column(self):
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Gender')
		self.assertContains(response, 'Phone number')
		self.assertContains(response, 'Amount spent')
		self.assertNotContains(response, 'Passenger')

	def test_add_customer_creates_customer_profile_without_password(self):
		image_data = BytesIO()
		Image.new('RGB', (1, 1), color='blue').save(image_data, format='PNG')
		image_data.seek(0)
		response = self.client.post(self.url, {
			'action': 'add',
			'first_name': 'Amina',
			'last_name': 'Nabirye',
			'phone_number': '+256772000001',
			'email': 'amina@example.com',
			'gender': 'female',
			'address': 'Kampala Central',
			'image': SimpleUploadedFile('amina.png', image_data.getvalue(), content_type='image/png'),
		})

		self.assertRedirects(response, self.url)
		customer = CustomerProfile.objects.get(user__email='amina@example.com')
		self.assertEqual(customer.user.role, 'customer')
		self.assertFalse(customer.user.has_usable_password())
		self.assertEqual(customer.user.gender, 'female')
		self.assertTrue(customer.user.image)
		self.assertEqual(customer.address, 'Kampala Central')
		customer.user.image.delete(save=False)

	def test_edit_customer_updates_profile_and_account(self):
		user = self.user_model.objects.create_user(
			phone_number='+256772000002',
			email='old@example.com',
			password='test-password',
			role='customer',
			first_name='Old',
			last_name='Name',
		)
		customer = CustomerProfile.objects.create(user=user, address='Old address')

		response = self.client.post(self.url, {
			'action': 'edit',
			'customer_id': customer.pk,
			'first_name': 'New',
			'last_name': 'Name',
			'phone_number': '+256772000002',
			'email': 'new@example.com',
			'gender': 'male',
			'address': 'New address',
		})

		self.assertRedirects(response, self.url)
		user.refresh_from_db()
		customer.refresh_from_db()
		self.assertEqual(user.full_name, 'New Name')
		self.assertEqual(user.email, 'new@example.com')
		self.assertEqual(user.gender, 'male')
		self.assertEqual(customer.address, 'New address')

	def test_directory_identifies_the_highest_spending_customer(self):
		customers = []
		for index, amount in enumerate((12000, 30000), start=2):
			user = self.user_model.objects.create_user(
				phone_number=f'+25677200000{index}',
				email=f'customer{index}@example.com',
				password='test-password',
				role='customer',
				first_name=f'Customer {index}',
			)
			customers.append(CustomerProfile.objects.create(user=user, address='Kampala'))
			CustomerPayment.objects.create(
				customer=customers[-1], amount=amount, payment_date=date.today(), payment_time=time(),
			)

		response = self.client.get(self.url)

		self.assertEqual(response.context['top_spender'], customers[1])
		self.assertEqual(response.context['top_spender'].amount_spent, 30000)
