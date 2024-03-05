from myproject.celery import app
from .services import UpdateAllowSpotTrading, UpdateSpotBookTicker


@app.task
def update_allow_spot_trading():
    return UpdateAllowSpotTrading().update_spot_trading_allow()

@app.task
def update_spot_book_ticker():
    return UpdateSpotBookTicker().update_spot_price()