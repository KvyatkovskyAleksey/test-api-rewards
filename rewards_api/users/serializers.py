from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import RewardLog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "coins")


class RewardLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardLog
        fields = ["id", "amount", "given_at"]


class RewardRequestSerializer(serializers.Serializer):

    def validate(self, attrs):
        return attrs
