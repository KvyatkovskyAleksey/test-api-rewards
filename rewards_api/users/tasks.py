from celery import shared_task

from .models import ScheduledReward, RewardLog


@shared_task
def execute_reward(scheduled_reward_id):
    try:
        reward = ScheduledReward.objects.get(id=scheduled_reward_id)
        reward.user.coins += reward.amount
        reward.user.save()

        RewardLog.objects.create(user=reward.user, amount=reward.amount)

    except ScheduledReward.DoesNotExist:
        pass
