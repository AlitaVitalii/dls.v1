import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'news-parser': {
        'task': 'pubdls.tasks.parser',
        'schedule': crontab(),
        # 'schedule': crontab(minute=0, hour='9, 17')  #
        # 'schedule': crontab(minute=0, hour='*/6')  # каждые 6 часов
        # 'schedule': crontab(minute=0, hour='1-23/2')  # каждый нечетный час
    },
}
