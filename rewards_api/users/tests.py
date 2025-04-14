from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser", password="testpassword123", coins=50
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.coins, 50)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_default_coins(self):
        user2 = self.User.objects.create_user(
            username="testuser2", password="testpassword456"
        )
        self.assertEqual(user2.coins, 0)

    def test_create_superuser(self):
        admin_user = self.User.objects.create_superuser(
            username="adminuser", password="adminpassword"
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
        self.assertEqual(admin_user.coins, 0)
