from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from itertools import groupby

from .models import OrderBookHistoryModel
from count.services import CountBookTicker


class TrackingLinks(CountBookTicker):
    def __init__(self) -> None:
        super().__init__()

    def process_positive_links(self, positive_links):
        profitable_links = {}

        for link in positive_links:
            spread = link['spread']
            if spread < 0.4:
                continue

            first_symbol = link['first']['symbol']
            second_symbol = link['second']['symbol']
            third_symbol = link['third']['symbol']

            unique_key = f'{first_symbol}--{second_symbol}--{third_symbol}'
            profitable_links[unique_key] = link

        return profitable_links

    def save_to_database(self, profitable_links):
        for unique_key, link in profitable_links.items():
            OrderBookHistoryModel.objects.create(
                spread=link['spread'],

                first_symbol=link['first']['symbol'],
                first_ask_price=link['first']['ask_price'],
                first_bid_price=link['first']['bid_price'],
                first_ask_qty=link['first']['ask_qty'],
                first_bid_qty=link['first']['bid_qty'],
                # first_order_book={"key1": "value1", "key2": "value2"},

                second_symbol=link['second']['symbol'],
                second_ask_price=link['second']['ask_price'],
                second_bid_price=link['second']['ask_price'],
                second_ask_qty=link['second']['ask_qty'],
                second_bid_qty=link['second']['bid_qty'],
                # second_order_book={"key3": "value3", "key4": "value4"},

                third_symbol=link['third']['symbol'],
                third_ask_price=link['third']['ask_price'],
                third_bid_price=link['third']['ask_price'],
                third_ask_qty=link['third']['ask_qty'],
                third_bid_qty=link['third']['bid_qty'],
                # third_order_book={"key5": "value5", "key6": "value6"},
            )

    def main(self) -> str:
        positive_links = cache.get(self.key_positive_links)
        if positive_links is None:
            return 'Данные для отслеживания прибыльных связок отсутствуют!'

        profitable_links = self.process_positive_links(positive_links)
        self.save_to_database(profitable_links)

        return f'Profitable links saved: {len(profitable_links)}'

    def get_data(self):
        end_date = timezone.now()
        start_date = end_date - timedelta(hours=12)
        order_book_history_data = OrderBookHistoryModel.objects \
            .filter(timestamp__range=(start_date, end_date))

        order_book_history_data = order_book_history_data \
            .order_by('first_symbol', 'second_symbol', 'third_symbol')

        grouped_data = {}
        for key, group in groupby(order_book_history_data, key=lambda x: (x.first_symbol, x.second_symbol, x.third_symbol)):
            grouped_data[key] = list(group)

        return grouped_data