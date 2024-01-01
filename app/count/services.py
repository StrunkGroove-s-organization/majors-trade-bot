from django.core.cache import cache
from parsing.services import UpdateSpotPrice, UpdateSpotBookTicker


class Count(UpdateSpotPrice):
    def __init__(self) -> None:
        super().__init__()
        self.positive_spread = []

    def count_spread(self, start_price: float, mid_price: float, end_price: float) -> float:
        spread = ((start_price * mid_price * end_price) - 1) * 100
        return spread

    def count(self, data: dict) -> None:
        for start_info in data:
            start_base = start_info['base']
            if start_base != 'USDT': continue
            start_quote = start_info['quote']

            for mid_info in data:
                mid_base = mid_info['base']
                if start_quote != mid_base: continue
                mid_quote = mid_info['quote']
                
                for end_info in data:
                    end_base = end_info['base']
                    if mid_quote != end_base: continue
                    end_quote = end_info['quote']
                    if end_quote != 'USDT': continue

                    spread = self.count_spread(
                        start_info['price'],
                        mid_info['price'],
                        end_info['price'],
                    )

                    if spread <= 0: continue
                    
                    record = {
                        'first': start_info,
                        'second': mid_info,
                        'third': end_info,
                        'spread': round(spread, 3),
                    }
                    self.positive_spread.append(record)

        self.positive_spread.sort(key=lambda x: x['spread'], reverse=True)

    def main(self) -> int:
        data = cache.get(self.key_spot_prices)

        self.count(data)

        cache.set(
            self.key_positive_links, 
            self.positive_spread, 
            self.time_spot_cache
        )
        return len(self.positive_spread)


class CountBookTicker(UpdateSpotBookTicker):
    def __init__(self) -> None:
        super().__init__()
        self.positive_spread = []

    def count_spread(self, start_price: float, mid_price: float, end_price: float) -> float:
        spread = ((start_price * mid_price * end_price) - 1) * 100
        return spread

    def get_price_by_symbol(self, coin: str, info: dict) -> float:
        if coin == info['base']:
            return info['quote'], info['bid_price']
        elif coin == info['quote']:
            return info['base'], info['ask_price']

    def count(self, data: dict) -> None:
        for start_info in data:
            start_base = start_info['base']
            start_quote = start_info['quote']
            if start_base != 'USDT': continue

            for mid_info in data:
                mid_base = mid_info['base']
                mid_quote = mid_info['quote']
                if start_quote != mid_base: continue
                
                for end_info in data:
                    end_base = end_info['base']
                    end_quote = end_info['quote']
                    if mid_quote != end_base: continue
                    if end_quote != start_base: continue
                    
                    get_start_coin, start_price = self.get_price_by_symbol(
                        coin='USDT',
                        info=start_info,
                    )
                    get_mid_coin, mid_price = self.get_price_by_symbol(
                        coin=get_start_coin,
                        info=mid_info,
                    )
                    get_end_coin, end_price = self.get_price_by_symbol(
                        coin=get_mid_coin,
                        info=end_info,
                    )
                    spread = self.count_spread(
                        start_price,
                        mid_price,
                        end_price,
                    )

                    if spread <= 0: continue
                    
                    record = {
                        'first': start_info,
                        'second': mid_info,
                        'third': end_info,
                        'spread': round(spread, 3),
                    }
                    self.positive_spread.append(record)

        self.positive_spread.sort(key=lambda x: x['spread'], reverse=True)

    def main(self) -> int:
        data = cache.get(self.key_spot_book_prices)

        self.count(data)

        cache.set(
            self.key_positive_links, 
            self.positive_spread, 
            self.time_spot_cache
        )
        return len(self.positive_spread)
