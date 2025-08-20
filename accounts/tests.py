from django.test import TestCase
from .models import User
from .forms import StudentRegistrationForm

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(email='test@example.com', first_name='Test', last_name='User', mobile='+123456789')
        self.assertEqual(user.get_full_name(), 'Test User')

class FormsTest(TestCase):
    def test_registration_form(self):
        form_data = {'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User', 'mobile': '+123456789', 'password1': 'pass123', 'password2': 'pass123'}
        form = StudentRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())