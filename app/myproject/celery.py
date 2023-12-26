import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {

    ### Parsing
    'parsing-spot-binance-task': {
        'task': 'parsing.tasks.binance',
        'schedule': 1,
    },

    ### Counting
    'count-spot-task': {
        'task': 'count.tasks.count',
        'schedule': 1,
    },
}