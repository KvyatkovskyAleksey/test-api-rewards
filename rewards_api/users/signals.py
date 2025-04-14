from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import ScheduledReward
from users.tasks import execute_reward


@receiver(post_save, sender=ScheduledReward)
def schedule_reward_task(sender, instance, created, **kwargs):
    if created:
        execute_reward.apply_async((instance.id,), eta=instance.execute_at)
