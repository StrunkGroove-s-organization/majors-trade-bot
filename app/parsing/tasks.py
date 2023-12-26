from myproject.celery import app
from .services import SpotBinance

@app.task
def binance():
    return SpotBinance().main()