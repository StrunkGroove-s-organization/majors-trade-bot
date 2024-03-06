from typing import Generator

import requests
from django.core.cache import cache

from .schemas import SymbolInfo, DataBookTicker
from .exceptions import MissingSpotTradingAllowError, MissingSpotPricesError


class RedisClass:
    def __init__(self) -> None:
        self.time_spot_cache = 30
        self.time_cache = 30


class BaseSpotBinance(RedisClass):
    def __init__(self) -> None:
        super().__init__()
        self.url_base = "https://api.binance.com"

    def get_requests(self, url: str) -> dict:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


class UpdateAllowSpotTrading(BaseSpotBinance):
    def __init__(self) -> None:
        super().__init__()
        self.__key_spot_trading_allow = "key_spot_trading_allow"
        self.__url_exchange_info = f"{self.url_base}/api/v1/exchangeInfo"
        self.__spot_trading_allow = {}

    def update_spot_trading_allow(self) -> int:
        data = self.get_requests(self.__url_exchange_info)
        for symbol_info in self.__spot_trading_symbols(data["symbols"]):
            self.__spot_trading_allow[symbol_info["symbol"]] = SymbolInfo(
                base=symbol_info["baseAsset"],
                quote=symbol_info["quoteAsset"],
            )
        self.__save()
        return len(self.__spot_trading_allow)

    @staticmethod
    def __spot_trading_symbols(data) -> Generator[dict, None, None]:
        for symbol_info in data:
            if symbol_info["status"] == "TRADING" \
            and symbol_info["isSpotTradingAllowed"] is True:
                yield symbol_info

    def get_allow_spot_trading(self) -> dict[str, SymbolInfo]:
        spot_trading_allow = cache.get(self.__key_spot_trading_allow)
        if isinstance(spot_trading_allow, dict):
            return spot_trading_allow
        
        self.update_spot_trading_allow()
        spot_trading_allow = cache.get(self.__key_spot_trading_allow)
        if isinstance(spot_trading_allow, dict):
            return spot_trading_allow
        
        raise MissingSpotTradingAllowError()

    def __save(self) -> None:
        cache.set(
            self.__key_spot_trading_allow,
            self.__spot_trading_allow, 
            self.time_spot_cache
        )


class UpdateSpotBookTicker(UpdateAllowSpotTrading):
    def __init__(self) -> None:
        super().__init__()
        self.__key_spot_book_prices = "key_spot_book_prices"
        self.__url_spot = f"{self.url_base}/api/v3/ticker/bookTicker"
        self.__allow_data = []

    def update_spot_price(self) -> int:
        for symbol_info, data_spot in self.allowed_data_generator():

            self.__allow_data.append(DataBookTicker(
                base=symbol_info.base,
                quote=symbol_info.quote,
                bid_price=data_spot["bidPrice"],
                bid_qty=data_spot["bidQty"],
                ask_price=data_spot["askPrice"],
                ask_qty=data_spot["askQty"],
            ))

            self.__allow_data.append(DataBookTicker(
                base=symbol_info.quote,
                quote=symbol_info.base,
                bid_price=data_spot["bidPrice"],
                bid_qty=data_spot["bidQty"],
                ask_price=data_spot["askPrice"],
                ask_qty=data_spot["askQty"],
                fake=True,
            ))
        
        self.__save()

        return len(self.__allow_data)

    def allowed_data_generator(self) -> Generator[tuple[SymbolInfo, dict], None, None]:
        data = self.get_requests(self.__url_spot)

        spot_trading_allow = self.get_allow_spot_trading()

        for data_spot in data:
            symbol = data_spot["symbol"]
            symbol_info = spot_trading_allow.get(symbol)
            if symbol_info is None: continue
            yield symbol_info, data_spot
    
    def get_spot_price(self) -> dict[str, DataBookTicker]:
        spot_prices = cache.get(self.__key_spot_book_prices)
        if isinstance(spot_prices, list):
            return spot_prices
        
        raise MissingSpotPricesError()
    
    def __save(self) -> None:
        cache.set(self.__key_spot_book_prices, self.__allow_data)