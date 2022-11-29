import os
from celery.schedules import crontab
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'APISwipe.settings')
app = Celery('APISwipe')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-every-day-in-00:00-for-activate': {
        'task': 'content.tasks.activate_user_subscription',
        'schedule': crontab(minute=0, hour=0),
    },

    'check-every-day-in-00:00-for-deactivate': {
        'task': 'content.tasks.deactivate_user_subscription',
        'schedule': crontab(minute=0, hour=0),
    },
    'check-every-day-in-00:00-for-deactivate_adv': {
        'task': 'content.tasks.deactivate_advertising',
        'schedule': crontab(minute=0, hour=0),
    },
}
app.conf.timezone = 'Europe/Kiev'