from datetime import date, time
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from accounts.models import CustomerProfile, DriverProfile
from api.models import CustomerPayment, Location, Trip, Vehicle


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

	def test_delete_customer_removes_trips_but_retains_unlinked_payment(self):
		user = self.user_model.objects.create_user(
			phone_number='+256772000008', email='delete-rider@example.com', password='test-password', role='customer',
		)
		customer = CustomerProfile.objects.create(user=user, address='Kampala')
		driver_user = self.user_model.objects.create_user(
			phone_number='+256772000009', email='delete-driver@example.com', password='test-password', role='driver',
		)
		driver = DriverProfile.objects.create(user=driver_user, date_of_birth=date(1990, 1, 1), address='Kampala')
		origin = Location.objects.create(name='Customer delete origin', lat='0.31', long='32.58')
		destination = Location.objects.create(name='Customer delete destination', lat='0.32', long='32.59')
		trip = Trip.objects.create(
			customer=customer, driver=driver, trip_date=date.today(), requested_at=time(10),
			origin=origin, destination=destination,
		)
		payment = CustomerPayment.objects.create(
			customer=customer, trip=trip, amount=12000, payment_date=date.today(), payment_time=time(10),
		)

		response = self.client.post(self.url, {'action': 'delete', 'customer_id': customer.pk})

		self.assertRedirects(response, self.url)
		self.assertFalse(CustomerProfile.objects.filter(pk=customer.pk).exists())
		self.assertFalse(Trip.objects.filter(pk=trip.pk).exists())
		payment.refresh_from_db()
		self.assertIsNone(payment.customer_id)
		self.assertIsNone(payment.trip_id)


class AdminManagementPagesTests(TestCase):
	def setUp(self):
		self.user_model = get_user_model()
		self.admin = self.user_model.objects.create_user(
			phone_number='+256700000009',
			email='pages-admin@example.com',
			password='test-password',
			role='admin',
		)
		self.client.force_login(self.admin)

	def make_trip_records(self):
		driver_user = self.user_model.objects.create_user(
			phone_number='+256700000012', email='records-driver@example.com', password='test-password', role='driver',
		)
		customer_user = self.user_model.objects.create_user(
			phone_number='+256700000013', email='records-rider@example.com', password='test-password', role='customer',
		)
		driver = DriverProfile.objects.create(user=driver_user, date_of_birth=date(1990, 1, 1), address='Kampala')
		customer = CustomerProfile.objects.create(user=customer_user, address='Kampala')
		origin = Location.objects.create(name='Record origin', lat='0.31', long='32.58')
		destination = Location.objects.create(name='Record destination', lat='0.32', long='32.59')
		vehicle = Vehicle.objects.create(
			driver=driver, plate_number='UAA 120A', name='City ride', model='Sedan', color='Black',
		)
		trip = Trip.objects.create(
			customer=customer, driver=driver, vehicle=vehicle, trip_date=date.today(),
			requested_at=time(10), origin=origin, destination=destination, status='completed',
		)
		payment = CustomerPayment.objects.create(
			customer=customer, trip=trip, amount=18000, payment_method='mtn_momo',
			payment_date=date.today(), payment_time=time(10),
		)
		return driver, customer, vehicle, origin, destination, trip, payment

	def test_driver_page_renders_empty_directory(self):
		response = self.client.get(reverse('admin_drivers'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Drivers Management Center')
		self.assertContains(response, 'No drivers have been added yet.')

	def test_trip_page_renders_both_charts_without_data(self):
		response = self.client.get(reverse('admin_trips'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Trips by month')
		self.assertContains(response, 'Trip status')
		self.assertEqual(len(response.context['trip_month_values']), 6)

	def test_earnings_page_renders_both_charts_without_data(self):
		response = self.client.get(reverse('admin_earnings'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Collected by month')
		self.assertContains(response, 'By payment method')
		self.assertEqual(len(response.context['earnings_month_values']), 6)

	def test_trip_and_payment_charts_include_current_month_totals(self):
		driver_user = self.user_model.objects.create_user(
			phone_number='+256700000010', email='driver@example.com', password='test-password', role='driver',
		)
		customer_user = self.user_model.objects.create_user(
			phone_number='+256700000011', email='rider@example.com', password='test-password', role='customer',
		)
		driver = DriverProfile.objects.create(user=driver_user, date_of_birth=date(1990, 1, 1), address='Kampala')
		customer = CustomerProfile.objects.create(user=customer_user, address='Kampala')
		origin = Location.objects.create(name='Origin', lat='0.31', long='32.58')
		destination = Location.objects.create(name='Destination', lat='0.32', long='32.59')
		vehicle = Vehicle.objects.create(
			driver=driver, plate_number='UAA 100A', name='City ride', model='Sedan', color='Black',
		)
		trip = Trip.objects.create(
			customer=customer, driver=driver, vehicle=vehicle, trip_date=date.today(),
			requested_at=time(10), origin=origin, destination=destination, status='completed',
		)
		CustomerPayment.objects.create(
			customer=customer, trip=trip, amount=18000, payment_method='mtn_momo',
			payment_date=date.today(), payment_time=time(10),
		)

		trip_response = self.client.get(reverse('admin_trips'))
		earnings_response = self.client.get(reverse('admin_earnings'))
		driver_response = self.client.get(reverse('admin_drivers'))

		self.assertEqual(trip_response.context['trip_month_values'][-1], 1)
		self.assertEqual(trip_response.context['completed_count'], 1)
		self.assertEqual(earnings_response.context['earnings_month_values'][-1], 18000)
		self.assertEqual(earnings_response.context['payment_method_values'][1], 18000)
		self.assertEqual(driver_response.context['drivers'][0].trip_count, 1)

	def test_driver_add_edit_and_delete(self):
		url = reverse('admin_drivers')
		data = {
			'action': 'add', 'first_name': 'Dina', 'last_name': 'Driver',
			'phone_number': '+256700000014', 'email': 'dina-driver@example.com',
			'gender': 'female', 'date_of_birth': '1992-04-03', 'address': 'Kampala',
		}
		response = self.client.post(url, data)
		self.assertRedirects(response, url)
		driver = DriverProfile.objects.get(user__email=data['email'])
		self.assertEqual(driver.user.role, 'driver')
		self.assertFalse(driver.user.has_usable_password())

		data.update(action='edit', driver_id=driver.pk, first_name='Diana', address='Entebbe')
		response = self.client.post(url, data)
		self.assertRedirects(response, url)
		driver.refresh_from_db()
		self.assertEqual(driver.user.first_name, 'Diana')
		self.assertEqual(driver.address, 'Entebbe')
		customer_user = self.user_model.objects.create_user(
			phone_number='+256700000015', email='driver-delete-rider@example.com', password='test-password', role='customer',
		)
		customer = CustomerProfile.objects.create(user=customer_user, address='Kampala')
		origin = Location.objects.create(name='Driver delete origin', lat='0.31', long='32.58')
		destination = Location.objects.create(name='Driver delete destination', lat='0.32', long='32.59')
		vehicle = Vehicle.objects.create(
			driver=driver, plate_number='UAA 140A', name='City ride', model='Sedan', color='Black',
		)
		trip = Trip.objects.create(
			customer=customer, driver=driver, vehicle=vehicle, trip_date=date.today(),
			requested_at=time(10), origin=origin, destination=destination,
		)
		payment = CustomerPayment.objects.create(
			customer=customer, trip=trip, amount=15000, payment_date=date.today(), payment_time=time(10),
		)

		self.client.post(url, {'action': 'delete', 'driver_id': driver.pk})
		self.assertFalse(DriverProfile.objects.filter(pk=driver.pk).exists())
		self.assertFalse(self.user_model.objects.filter(pk=driver.user_id).exists())
		self.assertFalse(Vehicle.objects.filter(pk=vehicle.pk).exists())
		self.assertFalse(Trip.objects.filter(pk=trip.pk).exists())
		payment.refresh_from_db()
		self.assertIsNone(payment.trip_id)

	def test_trip_edit_and_delete_preserves_unlinked_payment(self):
		_, customer, vehicle, origin, destination, trip, payment = self.make_trip_records()
		url = reverse('admin_trips')
		data = {
			'action': 'edit', 'trip_id': trip.pk, 'customer': customer.pk,
			'driver': trip.driver_id, 'vehicle': vehicle.pk, 'origin': origin.pk,
			'destination': destination.pk, 'trip_date': date.today().isoformat(),
			'requested_at': '11:30', 'status': 'cancelled',
		}
		response = self.client.post(url, data)
		self.assertRedirects(response, url)
		trip.refresh_from_db()
		self.assertEqual(trip.status, 'cancelled')
		self.assertEqual(trip.requested_at, time(11, 30))

		self.client.post(url, {'action': 'delete', 'trip_id': trip.pk})
		payment.refresh_from_db()
		self.assertIsNone(payment.trip_id)

	def test_payment_edit_and_delete(self):
		_, customer, _, _, _, trip, payment = self.make_trip_records()
		url = reverse('admin_earnings')
		data = {
			'action': 'edit', 'payment_id': payment.pk, 'customer': customer.pk,
			'trip': trip.pk, 'amount': 25000, 'payment_method': 'airtel_money',
			'payment_date': date.today().isoformat(), 'payment_time': '12:15',
		}
		response = self.client.post(url, data)
		self.assertRedirects(response, url)
		payment.refresh_from_db()
		self.assertEqual(payment.amount, 25000)
		self.assertEqual(payment.payment_method, 'airtel_money')

		self.client.post(url, {'action': 'delete', 'payment_id': payment.pk})
		self.assertFalse(CustomerPayment.objects.filter(pk=payment.pk).exists())
