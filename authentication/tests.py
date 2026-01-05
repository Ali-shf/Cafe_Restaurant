from django.test import TestCase
from django.contrib.auth import get_user_model
from authentication.models import (
    AdminProfile,
    CustomerProfile,
)

User = get_user_model() # CustomeUser model

# Create your tests here.

class CustomUserTestCase(TestCase):
    
    def test_create_user(self):
        params = {
            'username': 'ali-s',
            'first_name': 'ali',
            'last_name': 'sh',
            'age': 20,
            'email': 'ali@gmail.com',
            'birth_date': '2004-12-29',
        }
        user = User.objects.create(**params)
        self.assertEqual(user.username, 'ali-s')
        self.assertEqual(user.first_name, 'ali')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)



class AdminProfileTestCase(TestCase):
    user = User.objects.create(email='ali3@gmail.com', birth_date='2004-10-11')
    admin = AdminProfile.objects.create(user=user)
    
    def test_is_staff(self):
        self.assertTrue(self.admin.is_staff)
