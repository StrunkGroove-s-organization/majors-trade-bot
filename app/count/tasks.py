from myproject.celery import app
from .services import Count

@app.task
def count():
    return Count().main()