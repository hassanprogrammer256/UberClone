from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


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
