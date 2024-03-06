from datetime import timedelta
from itertools import groupby
from typing import Generator

from django.core.cache import cache
from django.utils import timezone

from parsing.services import UpdateSpotBookTicker
from parsing.schemas import DataBookTicker
from .schemas import ProfitLink
from .models import OrderBookHistoryModel
from .exceptions import MissingPositiveLinksError, MissingProfitLinksrror


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
        self.__positive_links = []
        self.__profitable_links = []

    def main(self) -> int:
        data = self.get_spot_price()
        
        self.__count(data)

        self.__save(self.__key_positive_links, self.__positive_links)
        self.__save(self.__key_profitable_links, self.__profitable_links)
        
        return len(self.__positive_links)

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

            self.__positive_links.append(profit_link)
            if spread < 0.4: continue
            self.__profitable_links.append(profit_link)

        self.__positive_links.sort(key=lambda x: x.spread, reverse=True)

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

    @property
    def positive_links(self) -> list[ProfitLink]:
        positive_links = cache.get(self.__key_positive_links)
        if isinstance(positive_links, list):
            return positive_links
        raise MissingPositiveLinksError()
    
    @property
    def profit_links(self) -> list[ProfitLink]:
        profit_links = cache.get(self.__key_profitable_links)
        if isinstance(profit_links, list):
            return profit_links
        raise MissingProfitLinksrror()


class AnalysisProfitLinks(CountBookTicker):
    def __init__(self) -> None:
        super().__init__()

    def save(self):
        for profit_link in self.profit_links:
            OrderBookHistoryModel.objects.create(
                spread=profit_link.spread,

                first_symbol=profit_link.first.symbol,
                first_ask_price=profit_link.first.ask_price,
                first_bid_price=profit_link.first.bid_price,
                first_ask_qty=profit_link.first.ask_qty,
                first_bid_qty=profit_link.first.bid_qty,

                second_symbol=profit_link.second.symbol,
                second_ask_price=profit_link.second.ask_price,
                second_bid_price=profit_link.second.ask_price,
                second_ask_qty=profit_link.second.ask_qty,
                second_bid_qty=profit_link.second.bid_qty,

                third_symbol=profit_link.third.symbol,
                third_ask_price=profit_link.third.ask_price,
                third_bid_price=profit_link.third.ask_price,
                third_ask_qty=profit_link.third.ask_qty,
                third_bid_qty=profit_link.third.bid_qty,
            )
        return len(self.profit_links)

    @property
    def analysis_data(self):
        end_date = timezone.now()
        start_date = end_date - timedelta(hours=2)
        order_book_history_data = OrderBookHistoryModel.objects \
            .filter(timestamp__range=(start_date, end_date))

        order_book_history_data = order_book_history_data \
            .order_by('first_symbol', 'second_symbol', 'third_symbol')

        grouped_data = {}
        for key, group in groupby(order_book_history_data, key=lambda x: (
            x.first_symbol, x.second_symbol, x.third_symbol
        )):
            grouped_data[key] = list(group)

        return grouped_data