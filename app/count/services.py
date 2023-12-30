from parsing.services import RedisClass
from django.core.cache import cache


class Count(RedisClass):
    def __init__(self) -> None:
        super().__init__()
        self.positive_spread = []

    def get_data(self, key: str):
        return cache.get(key)

    def count_spread(self, start_price: float, mid_price: float, end_price: float) -> float:
        spread = ((start_price * mid_price * end_price) - 1) * 100
        return spread

    def count(self, data: dict) -> None:
        data_usdt = self.get_data(self.key_spot_usdt_cache)

        for start_info in data_usdt.values():
            start_base = start_info['base']
            if start_base != 'USDT': continue
            start_quote = start_info['quote']
            start_bin_price = start_info['binance_price']

            for mid_info in data.values():
                mid_base = mid_info['base']
                if start_quote != mid_base: continue
                mid_quote = mid_info['quote']
                mid_bin_price = mid_info['binance_price']
                
                for end_info in data_usdt.values():
                    end_base = end_info['base']
                    if mid_quote != end_base: continue
                    end_quote = end_info['quote']
                    if end_quote != 'USDT': continue
                    end_bin_price = end_info['binance_price']

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

    def save(self):
        cache.set(
            self.key_positive_links, 
            self.positive_spread, 
            self.time_spot_cache
        )

    def main(self) -> int:
        data_bnb = self.get_data(self.key_spot_bnb_cache)
        data_btc = self.get_data(self.key_spot_btc_cache)
        data_fusdt = self.get_data(self.key_spot_fusdt_cache)
        data_tusdt = self.get_data(self.key_spot_tusdt_cache)

        dict_ads = {}
        dict_ads.update(data_bnb)
        dict_ads.update(data_btc)
        dict_ads.update(data_fusdt)
        dict_ads.update(data_tusdt)

        self.count(dict_ads)
        self.save()
        return len(self.positive_spread)
