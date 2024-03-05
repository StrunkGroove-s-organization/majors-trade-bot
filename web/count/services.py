from typing import Generator

from django.core.cache import cache

from parsing.services import UpdateSpotBookTicker
from parsing.schemas import DataBookTicker
from .schemas import ProfitLink


class ValidSymbolCombinations:
    @staticmethod
    def valid_symbol_combinations(data: list[DataBookTicker]) -> Generator[
        tuple[DataBookTicker, DataBookTicker, DataBookTicker], None, None
    ]:
        for start_info in ValidSymbolCombinations.__filter_start_symbols(
            data=data
        ):
            for mid_info in ValidSymbolCombinations.__filter_mid_symbols(
                data=data, start_quote=start_info.quote
            ):
                for end_info in ValidSymbolCombinations.__filter_end_symbols(
                    data=data, mid_quote=mid_info.quote, start_base=start_info.base
                ):
                    yield start_info, mid_info, end_info

    @staticmethod
    def __filter_start_symbols(data: list[DataBookTicker]
                             ) -> Generator[DataBookTicker, None, None]:
        for start_info in data:
            if start_info.base == 'USDT':
                yield start_info

    @staticmethod
    def __filter_mid_symbols(data: list[DataBookTicker], 
                             start_quote: str) -> Generator[DataBookTicker, None, None]:
        for mid_info in data:
            if mid_info.base == start_quote:
                yield mid_info

    @staticmethod
    def __filter_end_symbols(data: list[DataBookTicker], mid_quote: str,
                             start_base: str) -> Generator[DataBookTicker, None, None]:
        for end_info in data:
            if end_info.base == mid_quote and end_info.quote == start_base:
                yield end_info


class CountBookTicker(UpdateSpotBookTicker, ValidSymbolCombinations):
    def __init__(self) -> None:
        super().__init__()
        self.__key_positive_links = "key_positive_links"
        self.__key_profitable_links = "key_profitable_links"
        self.__positive_spread = []
        self.__profitable_spread = []

    def main(self) -> int:
        data = self.get_spot_price()
        
        self.__count(data)

        self.__save(self.__key_positive_links, self.__positive_spread)
        self.__save(self.__key_profitable_links, self.__profitable_spread)
        
        return len(self.__positive_spread)

    def __count(self, data: list[DataBookTicker]) -> None:
        for start_info, mid_info, end_info in self.valid_symbol_combinations(data):
            get_start_coin, start_price = self.__get_price_by_symbol(
                coin=start_info.base, info=start_info,
            )
            get_mid_coin, mid_price = self.__get_price_by_symbol(
                coin=get_start_coin, info=mid_info,
            )
            get_end_coin, end_price = self.__get_price_by_symbol(
                coin=get_mid_coin, info=end_info,
            )

            spread = self.__count_spread(start_price, mid_price, end_price)

            if spread <= 0: continue

            profit_link = ProfitLink(
                first=start_info,
                second=mid_info,
                third=end_info,
                spread=spread,
            )

            self.__positive_spread.append(profit_link)
            if spread < 0.4: continue
            self.__profitable_spread.append(profit_link)

        self.__positive_spread.sort(key=lambda x: x.spread, reverse=True)

    def __get_price_by_symbol(self, coin: str, info: DataBookTicker) -> tuple[str, float]:
        bid_price = info.bid_price
        ask_price = info.ask_price
        
        if info.fake is True:
            bid_price, ask_price = ask_price, bid_price

        if info.fake is not True:
            if coin == info.base:
                return info.quote, 1 / ask_price
            elif coin == info.quote:
                return info.base, 1 / bid_price

        else:
            if coin == info.base:
                return info.quote, ask_price
            elif coin == info.quote:
                return info.base, bid_price

    @staticmethod
    def __count_spread(start_price: float, mid_price: float, end_price: float) -> float:
        spread = ((start_price * mid_price * end_price) - 1) * 100
        return round(spread, 3)
    
    def __save(self, key: str, data: list) -> None:
        cache.set(key, data, self.time_spot_cache)

    def get_count_links(self) -> list[ProfitLink]:
        profit_links = cache.get(self.__key_positive_links)
        return profit_links