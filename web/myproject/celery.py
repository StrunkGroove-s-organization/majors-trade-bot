import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {

    ### Parsing
    'update-allow-spot-trading-task': {
        'task': 'parsing.tasks.update_allow_spot_trading',
        'schedule': crontab(hour=0, minute=0),
    },
    'update-spot-book-ticker-task': {
        'task': 'parsing.tasks.update_spot_book_ticker',
        'schedule': 1,
    },

    ### Counting
    'count-spot-task': {
        'task': 'count.tasks.count',
        'schedule': 1,
    },

    # ### Tracking
    # 'tracking-links-task': {
    #     'task': 'main.tasks.tracking_links',
    #     'schedule': 1,
    # },
}