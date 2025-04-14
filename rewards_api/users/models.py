from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    coins = models.IntegerField(default=0)


class ScheduledReward(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="scheduled_rewards"
    )
    amount = models.IntegerField()
    execute_at = models.DateTimeField()

    class Meta:
        ordering = ["execute_at"]
        verbose_name = "Scheduled Reward"
        verbose_name_plural = "Scheduled Rewards"

    def __str__(self):
        return (
            f"Reward {self.amount} coins for {self.user.username} at {self.execute_at}"
        )
