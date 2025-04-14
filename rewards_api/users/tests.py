from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import ScheduledReward, RewardLog, CustomUser, UserRewardRequest
from users.tasks import execute_reward


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


class UserProfileAPITests(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        # Создаем тестового пользователя
        self.user = self.User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
            coins=150,
        )
        self.profile_url = reverse("user_profile")

    def test_get_profile_authenticated(self):
        # Логиним пользователя
        self.client.force_authenticate(self.user)

        # Делаем GET-запрос
        response = self.client.get(self.profile_url)

        # Проверяем, успешен ли запрос
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"username": "testuser", "email": "testuser@example.com", "coins": 150},
        )

    def test_get_profile_unauthenticated(self):
        # Делаем GET-запрос без авторизации
        response = self.client.get(self.profile_url)

        # Проверяем, что доступ запрещён (возвращает HTTP 401 Unauthorized или 403 Forbidden)
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )


class ScheduledRewardTaskTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(  # noqa
            username="tasktestuser",
            email="tasktestuser@example.com",
            password="testpassword123",
            coins=100,
        )

        self.reward = ScheduledReward.objects.create(
            user=self.user, amount=50, execute_at=timezone.now()
        )

    def test_execute_reward_task(self):
        # вызываем задачу вручную (синхронно)
        execute_reward(self.reward.id)

        # проверим, что пользователь получил монеты
        self.user.refresh_from_db()
        self.assertEqual(self.user.coins, 150)

        # убедимся, что была создана запись RewardLog
        reward_log = RewardLog.objects.filter(user=self.user, amount=50).first()
        self.assertIsNotNone(reward_log)


class RewardRequestViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="rewarduser", email="user@test.com", password="testpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # noqa

    def test_user_can_request_reward(self):
        response = self.client.post("/api/rewards/request/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверка наличия записи после вызова
        request_exists = UserRewardRequest.objects.filter(
            user=self.user, date=timezone.now().date()
        ).exists()
        self.assertTrue(request_exists)

    def test_user_cannot_request_twice_in_one_day(self):
        UserRewardRequest.objects.create(user=self.user, date=timezone.now().today())
        response = self.client.post("/api/rewards/request/")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(
            response.data["detail"], "You have already requested a reward today."
        )
