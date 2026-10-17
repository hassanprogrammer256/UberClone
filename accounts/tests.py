from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import override_settings
from .models import CustomUser

class AccountsTestCase(TestCase):

    def test_register_view(self):
        get_response = self.client.get('/auth/register/')
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'auth/register.html')
        print("Register GET view test passed.")
        post_response = self.client.post('/auth/register/', {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',}
        )
        self.assertEqual(post_response.status_code, 200)
        print("Register POST view test passed.")



    def test_login_view(self):
        get_response = self.client.get('/auth/login/')
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'auth/login.html')
        print("Login GET view test passed.")
        post_response = self.client.post('/auth/login/', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(post_response.status_code, 200)
        print("Login POST view test passed.")

    def test_login_with_email(self):
        user = CustomUser.objects.create_user(
            username='emailuser',
            email='Driver@example.com',
            password='StrongPass123!',
            phone_number='+256700123456',
        )

        response = self.client.post('/auth/login/', {
            'username': 'Driver@example.com',
            'password': 'StrongPass123!',
        })

        self.assertRedirects(response, '/')
        self.assertEqual(response.wsgi_request.user.pk, user.pk)

    def test_login_with_local_phone_number(self):
        user = CustomUser.objects.create_user(
            username='phoneuser',
            email='phoneuser@example.com',
            password='StrongPass123!',
            phone_number='+256700123456',
        )

        response = self.client.post('/auth/login/', {
            'username': '0700123456',
            'password': 'StrongPass123!',
        })

        self.assertRedirects(response, '/')
        self.assertEqual(response.wsgi_request.user.pk, user.pk)

    def test_login_with_username_still_works(self):
        user = CustomUser.objects.create_user(
            username='existinguser',
            email='existinguser@example.com',
            password='StrongPass123!',
        )

        response = self.client.post('/auth/login/', {
            'username': user.username,
            'password': 'StrongPass123!',
        })

        self.assertRedirects(response, '/')
        self.assertEqual(response.wsgi_request.user.pk, user.pk)

    def test_invalid_login_keeps_password_step_open(self):
        CustomUser.objects.create_user(
            username='retryuser',
            email='retry@example.com',
            password='StrongPass123!',
        )

        response = self.client.post('/auth/login/', {
            'username': 'retry@example.com',
            'password': 'incorrect-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password.')
        self.assertNotContains(response, 'id="password-step" hidden')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_registered_user_can_sign_in_with_email(self):
        password = 'StrongPass123!'
        registration_response = self.client.post('/auth/register/', {
            'username': 'newDriver@example.com',
            'email': 'newDriver@example.com',
            'first_name': 'New',
            'last_name': 'Driver',
            'phone_number': '0700123456',
            'password': password,
            'confirm_password': password,
            'terms': 'on',
        })

        self.assertRedirects(registration_response, '/auth/login/')
        user = CustomUser.objects.get(email='newDriver@example.com')
        self.assertTrue(user.check_password(password))

        login_response = self.client.post('/auth/login/', {
            'username': 'newDriver@example.com',
            'password': password,
        })

        self.assertRedirects(login_response, '/')
        self.assertEqual(login_response.wsgi_request.user.pk, user.pk)

    def test_registration_enforces_terms_and_password_requirements(self):
        response = self.client.post('/auth/register/', {
            'email': 'policyuser@example.com',
            'first_name': 'Policy',
            'last_name': 'User',
            'password': 'passwordonly',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('terms', response.context['form'].errors)
        self.assertIn('password', response.context['form'].errors)
        self.assertFalse(CustomUser.objects.filter(email='policyuser@example.com').exists())

    def test_registration_uploads_profile_photo(self):
        image_file = BytesIO()
        Image.new('RGB', (8, 8), color='blue').save(image_file, format='PNG')
        image_file.seek(0)
        uploaded_image = SimpleUploadedFile(
            'avatar.png', image_file.read(), content_type='image/png'
        )

        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            response = self.client.post('/auth/register/', {
                'email': 'avataruser@example.com',
                'first_name': 'Avatar',
                'last_name': 'User',
                'password': 'StrongPass123!',
                'confirm_password': 'StrongPass123!',
                'terms': 'on',
                'image': uploaded_image,
            })

            self.assertRedirects(response, '/auth/login/')
            user = CustomUser.objects.get(email='avataruser@example.com')
            self.assertTrue(user.image.name.startswith('profile_images/'))
            self.assertTrue(user.image.storage.exists(user.image.name))

    def test_registration_rejects_mismatched_passwords(self):
        response = self.client.post('/auth/register/', {
            'email': 'mismatch@example.com',
            'first_name': 'Mismatch',
            'last_name': 'Password',
            'password': 'StrongPass123!',
            'confirm_password': 'DifferentPass123!',
            'terms': 'on',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('confirm_password', response.context['form'].errors)
        self.assertFalse(CustomUser.objects.filter(email='mismatch@example.com').exists())

