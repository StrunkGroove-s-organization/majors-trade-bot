import requests

from django.core.cache import cache


class RedisClass:
    def __init__(self) -> None:
        self.time_spot_cache = 30
        self.time_cache = 30


class BaseSpotBinance(RedisClass):
    def __init__(self) -> None:
        super().__init__()
        self.url_base = "https://api.binance.com"
        self.tickers = {}

    def get_requests(self, url: str) -> dict:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.json()


class UpdateSpotTradingList(BaseSpotBinance):
    def __init__(self):
        super().__init__()
        self.key_spot_trading_allow = "key_spot_trading_allow"
        self.url_exchange_info = f"{self.url_base}/api/v1/exchangeInfo"
        self.spot_trading_allow = {}

    def update_spot_trading_list(self) -> int:
        data = self.get_requests(self.url_exchange_info)
        if not data: return f"Binance wrong requests ({self.url_exchange_info})"

        for symbol_info in data["symbols"]:
            status = symbol_info["status"]
            is_trading_spot = symbol_info["isSpotTradingAllowed"]
            
            if status == "TRADING" and is_trading_spot == True:
                self.spot_trading_allow[symbol_info["symbol"]] = {
                    "base": symbol_info["baseAsset"],
                    "quote": symbol_info["quoteAsset"],
                }

        cache.set(
            self.key_spot_trading_allow,
            self.spot_trading_allow, 
            self.time_spot_cache
        )

        return len(self.spot_trading_allow)


class UpdateSpotPrice(UpdateSpotTradingList):
    def __init__(self) -> None:
        super().__init__()
        self.key_spot_prices = "key_spot_prices"
        self.url_spot = f"{self.url_base}/api/v3/ticker/price"
        self.allow_data = []

    def update_spot_price(self) -> int:
        data = self.get_requests(self.url_spot)
        if not data: return f"Binance wrong requests ({self.url_spot})"

        spot_trading_allow = cache.get(self.key_spot_trading_allow)
        if not spot_trading_allow: 
            self.update_spot_trading_list()
            spot_trading_allow = cache.get(self.key_spot_trading_allow)
            if not spot_trading_allow:  return f"Missing spot_trading_allow set"

        for data_spot in data:
            symbol = data_spot["symbol"]
            symbol_info = spot_trading_allow.get(symbol)

            if symbol_info is None: continue

            self.allow_data.append({
                "symbol": symbol,
                "price": float(data_spot["price"]),
                "binance_price": float(data_spot["price"]),
                "base": symbol_info["base"],
                "quote": symbol_info["quote"],
            })
            self.allow_data.append({
                "symbol": symbol_info["quote"] + symbol_info["base"],
                "price": 1 / float(data_spot["price"]),
                "binance_price": float(data_spot["price"]),
                "base": symbol_info["quote"],
                "quote": symbol_info["base"],
                "fake": True,
            })
        
        cache.set(
            self.key_spot_prices,
            self.allow_data
        )
        return len(self.allow_data)


class UpdateSpotBookTicker(UpdateSpotTradingList):
    def __init__(self) -> None:
        super().__init__()
        self.key_spot_book_prices = "key_spot_book_prices"
        self.url_spot = f"{self.url_base}/api/v3/ticker/bookTicker"
        self.allow_data = []

    def update_spot_price(self) -> int:
        data = self.get_requests(self.url_spot)
        if not data: return f"Binance wrong requests ({self.url_spot})"

        spot_trading_allow = cache.get(self.key_spot_trading_allow)
        if not spot_trading_allow: 
            self.update_spot_trading_list()
            spot_trading_allow = cache.get(self.key_spot_trading_allow)
            if not spot_trading_allow:  return f"Missing spot_trading_allow set"

        for data_spot in data:
            symbol = data_spot["symbol"]
            symbol_info = spot_trading_allow.get(symbol)

            if symbol_info is None: continue

            self.allow_data.append({
                "symbol": symbol,

                "bid_price": float(data_spot["bidPrice"]),
                "bid_qty": float(data_spot["bidQty"]),
                "ask_price": float(data_spot["askPrice"]),
                "ask_qty": float(data_spot["askQty"]),

                "base": symbol_info["base"],
                "quote": symbol_info["quote"],
            })
            self.allow_data.append({
                "symbol": symbol_info["quote"] + symbol_info["base"],

                "bid_price": 1 / float(data_spot["bidPrice"]),
                "bid_qty": float(data_spot["bidQty"]),
                "ask_price": 1 / float(data_spot["askPrice"]),
                "ask_qty": float(data_spot["askQty"]),

                "base": symbol_info["quote"],
                "quote": symbol_info["base"],
                "fake": True,
            })
        
        cache.set(
            self.key_spot_book_prices,
            self.allow_data
        )
        return len(self.allow_data)
    

class CheckPriceBinanceBySymbol(UpdateSpotPrice):
    def __init__(self, symbol: str) -> None:
        super().__init__()
        self.symbol = symbol.upper()
        self.symbol_info = []

    def find_symbol(self, data: dict) -> list:
        for symbol_info in data:
            symbol = symbol_info["symbol"]

            if symbol == self.symbol:
                self.symbol_info.append(symbol_info)

        if len(self.symbol_info) == 0:
            return None
        return self.symbol_info
    
    def main(self) -> list:
        data = self.get_requests(self.url_spot)
        info = self.find_symbol(data)
        return info