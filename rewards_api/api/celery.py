from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

app = Celery("api")

app.conf.timezone = "UTC"
app.conf.beat_schedule = {
    # "check_scrapyd": {"task": "core.tasks.check_scrapyd_jobs", "schedule": 10.0},
    # "nba_run_spiders": {
    #     "task": "nba.tasks.nba_run_spiders",
    #     "schedule": crontab(hour="*", minute="30"),
    # },
    # "prepare_nba_data": {
    #     "task": "nba.tasks.prepare_nba_dataframe",
    #     "schedule": crontab(hour="*", minute="45"),
    # },
    # "wnba_run_spiders": {
    #     "task": "wnba.tasks.wnba_run_spiders",
    #     "schedule": crontab(hour="*", minute="25"),
    # },
    # "prepare_wnba_data": {
    #     "task": "wnba.tasks.prepare_wnba_dataframe",
    #     "schedule": crontab(hour="*", minute="40"),
    # },
}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
