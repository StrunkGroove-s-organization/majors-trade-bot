import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {

    ### Parsing
    'update-spot-price-task': {
        'task': 'parsing.tasks.update_spot_price',
        'schedule': 1,
    },
    'update-spot-trading-list-task': {
        'task': 'parsing.tasks.update_spot_trading_list',
        'schedule': crontab(hour=0, minute=0),
    },

    ### Counting
    # 'count-spot-task': {
    #     'task': 'count.tasks.count',
    #     'schedule': 1,
    # },
}