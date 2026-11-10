import io
from contextlib import redirect_stdout
from io import StringIO
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from api.models import Location
from accounts.models import CustomerProfile, DriverProfile


class CustomSuperuserCommandTests(TestCase):
	@patch('accounts.management.commands.createcustomsuperuser.getpass', side_effect=['Secure-test-pass-2026!', 'Secure-test-pass-2026!'])
	@patch('builtins.input', side_effect=['admin@example.com', '+256700000777'])
	def test_command_creates_admin_superuser(self, mocked_input, mocked_getpass):
		output = StringIO()

		call_command('createcustomsuperuser', stdout=output)

		user = get_user_model().objects.get(email='admin@example.com')
		self.assertEqual(user.phone_number, '+256700000777')
		self.assertEqual(user.role, 'admin')
		self.assertTrue(user.is_staff)
		self.assertTrue(user.is_superuser)
		self.assertTrue(user.check_password('Secure-test-pass-2026!'))
		self.assertIn('created successfully', output.getvalue())


class RegistrationTests(TestCase):
	def setUp(self):
		self.location = Location.objects.create(name='Kampala', lat='0.3476', long='32.5825')

	def test_registration_form_uses_locations_from_database(self):
		response = self.client.get(reverse('register'), {'role': 'driver'})

		self.assertEqual(response.status_code, 200)
		self.assertQuerySetEqual(
			response.context['form'].fields['location'].queryset,
			[repr(self.location)],
			transform=repr,
		)
		self.assertContains(response, 'name="image"')
		self.assertContains(response, 'name="first_name"')
		self.assertContains(response, 'name="email"')
		self.assertContains(response, 'name="role" value="driver"')

	def test_registration_creates_user_and_saves_selected_location(self):
		image_data = io.BytesIO()
		Image.new('RGB', (1, 1), color='white').save(image_data, format='PNG')

		with TemporaryDirectory() as media_root:
			with self.settings(MEDIA_ROOT=media_root):
				response = self.client.post(
						reverse('register') + '?role=driver',
					{
						'first_name': 'Alex',
						'last_name': 'Rider',
						'email': 'alex@example.com',
						'phone_number': '+256700000321',
						'date_of_birth': '1990-01-01',
						'password': 'Long-enough!2026',
						'confirm_password': 'Long-enough!2026',
						'location': str(self.location.pk),
						'terms': 'on',
						'image': SimpleUploadedFile(
							'profile.png', image_data.getvalue(), content_type='image/png'
						),
					},
				)

				self.assertRedirects(response, reverse('login'))
				user = get_user_model().objects.get(email='alex@example.com')
				self.assertEqual(user.first_name, 'Alex')
				self.assertEqual(user.role, 'driver')
				self.assertTrue(user.check_password('Long-enough!2026'))
				self.assertTrue(user.image.storage.exists(user.image.name))
				profile = DriverProfile.objects.get(user=user)
				self.assertEqual(profile.address, 'Kampala')
				self.assertEqual(str(profile.date_of_birth), '1990-01-01')

	def test_customer_role_from_query_creates_customer_profile(self):
		response = self.client.post(
			reverse('register') + '?role=customer',
			{
				'role': 'driver',
				'first_name': 'Casey',
				'last_name': 'Passenger',
				'email': 'casey@example.com',
				'phone_number': '+256700000654',
				'password': 'Long-enough!2026',
				'confirm_password': 'Long-enough!2026',
				'location': str(self.location.pk),
				'terms': 'on',
			},
		)

		self.assertRedirects(response, reverse('login'))
		user = get_user_model().objects.get(email='casey@example.com')
		self.assertEqual(user.role, 'customer')
		self.assertEqual(CustomerProfile.objects.get(user=user).address, 'Kampala')
		self.assertFalse(DriverProfile.objects.filter(user=user).exists())

	def test_invalid_registration_shows_message_and_prints_errors(self):
		terminal_output = StringIO()

		with redirect_stdout(terminal_output):
			response = self.client.post(reverse('register') + '?role=customer', {})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'data-server-snackbar')
		self.assertContains(response, 'Please correct the highlighted errors and try again.')
		self.assertContains(response, 'This field is required.')
		self.assertIn('Registration validation failed (role=customer)', terminal_output.getvalue())
		self.assertIn('This field is required.', terminal_output.getvalue())


class LoginSnackbarTests(TestCase):
	def test_failed_login_shows_error_snackbar(self):
		response = self.client.post(
			reverse('login'),
			{'username': 'missing@example.invalid', 'password': 'incorrect'},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'data-server-snackbar')
		self.assertContains(response, 'data-type="error"')
		self.assertContains(response, 'Sign-in failed.')

	def test_successful_login_shows_success_snackbar_after_redirect(self):
		user = get_user_model().objects.create_user(
			phone_number='+256700000123',
			email='snackbar-test@example.com',
			password='test-password-123',
		)

		response = self.client.post(
			reverse('login'),
			{
				'username': user.email,
				'password': 'test-password-123',
				'next': '/',
			},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'data-server-snackbar')
		self.assertContains(response, 'data-type="success"')
		self.assertContains(response, 'You are signed in.')
