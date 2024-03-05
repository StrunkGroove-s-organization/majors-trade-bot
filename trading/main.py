import requests

from os import getenv
from time import sleep

from binance.spot import Spot as Client

class Binance:
    def __init__(self):
        self.api_key = getenv("PUBLIC")
        self.api_secret = getenv("SECRET")
        self.spot_client = Client(self.api_key, self.api_secret)

    def get_profitable_links(self):
        url = "http://web:8000/api/v1/profitable-links-binance"
        response = requests.get(url)

    def get_spot_balance(self):
        for balance in self.spot_client.balance():
            if balance["walletName"] == "Spot":
                return balance["balance"]

    def create_order(self):
        params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "MARKET",
            "quantity": 0.00020,
        }
        response = self.spot_client.new_order(**params)
        print(response)
        return response

sleep(10)
binance = Binance()
data = binance.create_order()
