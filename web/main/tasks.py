from myproject.celery import app
from .services import TrackingLinks

@app.task
def tracking_links():
    return TrackingLinks().main()