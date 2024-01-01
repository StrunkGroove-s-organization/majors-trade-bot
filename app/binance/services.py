import requests
import time
import hashlib
import hmac

from os import getenv


api_key = getenv('API_PUBLIC')
api_secret = getenv('API_SECRET')


class BaseBinance:
    def __init__(self) -> None:
        self.base_url = 'https://api.binance.com'
        self.recv_window = 5000

    def get_headers(self) -> dict:
        return {'X-MBX-APIKEY': api_key}
    
    def get_timestamp(self) -> int:
        return int(time.time() * 1000)

    def get_signature(self, query: str) -> str:
        return hmac.new(
            api_secret.encode('utf-8'), 
            query.encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()


class BinanceActions(BaseBinance):
    def check_balance(self) -> dict:
        query = f"recvWindow={self.recv_window} \
            &timestamp={self.get_timestamp()}"
        
        signature = self.get_signature(query)
        url = f"{self.base_url}/api/v3/account?{query}&signature={signature}"
        response = requests.get(url, headers=self.get_headers())

        if response.status_code != 200:
            return {"error": f"Error {response.status_code}: {response.text}"}
        
        balance = response.json()
        return balance

    def create_order(self, symbol: str, side: str, quantity: float) -> dict:
        query = (
            f"symbol={symbol}"
            f"&side={side}"
            f"&type=MARKET"
            f"&quantity={quantity}"
            f"&recvWindow={self.recv_window}"
            f"&timestamp={self.get_timestamp()}"
            f"&newOrderRespType=FULL"
        )
        
        signature = self.get_signature(query)
        url = f"{self.base_url}/api/v3/order?{query}&signature={signature}"
        response = requests.post(url, headers=self.get_headers())

        if response.status_code != 200:
            return {"error": f"Error {response.status_code}: {response.text}"}

        info = response.json()
        return info

    def test_order(self, symbol: str, side: str, quantity: float) -> dict:
        query = (
            f"symbol={symbol}"
            f"&side={side}"
            f"&type=MARKET"
            f"&quantity={quantity}"
            f"&recvWindow={self.recv_window}"
            f"&timestamp={self.get_timestamp()}"
            f"&newOrderRespType=FULL"
            f"&computeCommissionRates=true"
        )
        signature = self.get_signature(query)
        url = f"{self.base_url}/api/v3/order/test?{query}&signature={signature}"
        response = requests.post(url, headers=self.get_headers())

        if response.status_code != 200:
            return {"error": f"Error {response.status_code}: {response.text}"}

        info = response.json()
        return info

    def check_order(self, symbol: str) -> dict:
        query = f"symbol={symbol} \
            &recvWindow={self.recv_window} \
            &timestamp={self.get_timestamp()}"
        
        signature = self.get_signature(query)
        url = f"{self.base_url}/api/v3/myTrades?{query}&signature={signature}"

        response = requests.get(url, headers=self.get_headers())

        if response.status_code != 200:
            return {"error": f"Error {response.status_code}: {response.text}"}
        
        info = response.json()
        return info

    def order_book(self, symbol: str, limit=5) -> dict:
        params = {'symbol': symbol, 'limit': limit}
        url = f"{self.base_url}/api/v3/depth"
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return {"error": f"Error {response.status_code}: {response.text}"}
        
        order_book = response.json()
        return order_book

    def __init__(self) -> None:
        self.base_url = 'https://api.binance.com'
        self.recv_window = 5000

    def get_headers(self) -> dict:
        return {'X-MBX-APIKEY': api_key}
    
    def get_timestamp(self) -> int:
        return int(time.time() * 1000)

    def get_signature(self, query: str) -> str:
        signature = hmac.new(api_secret.encode('utf-8'), 
                             query.encode('utf-8'), 
                             hashlib.sha256).hexdigest()
        return signature
                                                                                      
    def check_balance(self) -> dict:
        query = f"recvWindow={self.recv_window} \
            &timestamp={self.get_timestamp()}"
        
        signature = self.get_signature(query)
        url = f"{self.base_url}/api/v3/account?{query}&signature={signature}"

        response = requests.get(url, headers=self.get_headers())

        if response.status_code != 200:
            return {"error": f"Error {response.status_code}: {response.text}"}
        
        balance = response.json()
        return balance

    def create_order(self, symbol: str, site: str, quantity: float) -> dict:
        query = f"symbol={symbol} \
            &side={site} \
            &type=MARKET \
            &quantity={quantity} \
            &recvWindow={self.recv_window} \
            &timestamp={self.get_timestamp()} \
            &newOrderRespType=FULL"
        
        signature = self.get_signature(query)
        url = f"{self.base_url}/api/v3/order?{query}&signature={signature}"
        response = requests.post(url, headers=self.get_headers())

        if response.status_code != 200:
            return {"error": f"Error {response.status_code}: {response.text}"}

        info = response.json()
        return info

    def test_order(self) -> dict:
        query = f"symbol={'BTCUSDT'} \
            &side={'SELL'} \
            &type=MARKET \
            &quantity={1} \
            &recvWindow={self.recv_window} \
            &timestamp={self.get_timestamp()} \
            &newOrderRespType=FULL"
        
        signature = self.get_signature(query)
        url = f"{self.base_url}/api/v3/order?{query}&signature={signature}"
        response = requests.post(url, headers=self.get_headers())

        if response.status_code != 200:
            return {"error": f"Error {response.status_code}: {response.text}"}

        info = response.json()
        return info

    def check_order(self, symbol: str) -> dict:
        query = f"symbol={symbol} \
            &recvWindow={self.recv_window} \
            &timestamp={self.get_timestamp()}"
        
        signature = self.get_signature(query)
        url = f"{self.base_url}/api/v3/myTrades?{query}&signature={signature}"

        response = requests.get(url, headers=self.get_headers())

        if response.status_code != 200:
            return {"error": f"Error {response.status_code}: {response.text}"}
        
        info = response.json()
        return info
    
    def order_book(self, symbol: str, limit=5) -> dict:
        params = {'symbol': symbol, 'limit': limit}
        url = f"{self.base_url}/api/v3/depth"
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return {"error": f"Error {response.status_code}: {response.text}"}
        
        order_book = response.json()
        return order_book