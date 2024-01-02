from myproject.celery import app
from .services import Count, CountBookTicker

@app.task
def count():
    return CountBookTicker().main()