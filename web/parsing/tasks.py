from myproject.celery import app
from .services import UpdateSpotPrice, UpdateSpotBookTicker, UpdateSpotTradingList


@app.task
def update_spot_price():
    # return UpdateSpotPrice().update_spot_price()
    return UpdateSpotBookTicker().update_spot_price()

@app.task
def update_spot_trading_list():
    return UpdateSpotTradingList().update_spot_trading_list()