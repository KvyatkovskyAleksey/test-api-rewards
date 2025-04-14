from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import RewardLog, ScheduledReward, CustomUser, UserRewardRequest
from .serializers import UserSerializer, RewardLogSerializer, RewardRequestSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class RewardLogListView(generics.ListAPIView):
    serializer_class = RewardLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращаем только награды авторизованного пользователя
        return RewardLog.objects.filter(user=self.request.user).order_by("-given_at")


class RewardRequestView(generics.GenericAPIView):
    serializer_class = RewardRequestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        reward_amount = settings.USER_REQUEST_REWARD_AMOUNT

        # Проверка на существование запроса в текущий день
        if reward_was_requested_before(user):
            return Response(
                {"detail": "You have already requested a reward today."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        reward_execute_at = timezone.now() + timedelta(minutes=5)
        ScheduledReward.objects.create(
            user=user, amount=reward_amount, execute_at=reward_execute_at
        )

        UserRewardRequest.objects.create(user=user, date=timezone.now().date())

        return Response(
            {
                "detail": f"Reward of {reward_amount} coins scheduled for execution at {reward_execute_at}"
            },
            status=status.HTTP_201_CREATED,
        )


def reward_was_requested_before(user: CustomUser) -> bool:
    today = timezone.now().date()
    return UserRewardRequest.objects.filter(user=user, date=today).exists()
