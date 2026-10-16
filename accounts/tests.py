from django.test import TestCase

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

