import os
import requests
import time
import hashlib
import hmac


api_key = os.getenv('API_PUBLIC')
api_secret = os.getenv('API_SECRET')


class BinanceActions:
    def __init__(self) -> None:
        self.base_url = 'https://api.binance.com'
        self.recv_window = 5000

    def get_headers(self) -> dict:
        return {'X-MBX-APIKEY': api_key}
    
    def get_timestamp(self) -> int:
        timestamp = int(time.time() * 1000)
        return timestamp

    def get_signature(self, query: str) -> str:
        signature = hmac.new(api_secret.encode('utf-8'), 
                             query.encode('utf-8'), 
                             hashlib.sha256).hexdigest()
        return signature
                                                                                      
    def check_balance(self) -> dict:
        query = f"recvWindow={self.recv_window}&timestamp={self.get_timestamp}"
        signature = self.get_signature(query)
        url = f"{self.base_url}/api/v3/account?{query}&signature={signature}"

        response = requests.get(url, headers=self.get_headers)

        if response.status_code != 200:
            return None
        
        balance = response.json()
        return balance

    def exchange(self, base_currency: str, quote_currency: str,
                 quantity: float, order_type: str) -> dict:
        symbol = f"{base_currency}{quote_currency}"
        query = f"symbol={symbol}&side={order_type}&type=MARKET&quantity={quantity}&recvWindow={self.recv_window}&timestamp={self.get_timestamp()}&newOrderRespType=FULL"
        signature = self.get_signature(query)
        url = f"{self.base_url}/api/v3/order?{query}&signature={signature}"

        response = requests.post(url, headers=self.get_headers)

        if response.status_code != 200:
            return None

        info = response.json()
        return info

    def check_order(self, symbol: str) -> dict:
        query = f"symbol={symbol}&recvWindow={self.recv_window}&timestamp={self.get_timestamp()}"
        signature = self.get_signature(query)
        url = f"{self.base_url}/api/v3/myTrades?{query}&signature={signature}"

        response = requests.get(url, headers=self.get_headers)

        if response.status_code != 200:
            return None
        
        info = response.json()
        return info
    
    def order_book(self, symbol: str, limit=5) -> dict:
        endpoint = '/api/v3/depth'

        params = {'symbol': symbol, 'limit': limit}

        response = requests.get(self.base_url + endpoint, params=params)

        if response.status_code != 200:
            return None
        
        order_book = response.json()
        return order_book