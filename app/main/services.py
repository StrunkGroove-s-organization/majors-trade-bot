from parsing.services import SpotBinance


class CheckPriceBinance(SpotBinance):
    def __init__(self, ticker: str) -> None:
        super().__init__()
        self.ticker = ticker.upper()

    def find_ticker(self, data: dict) -> list:
        tickers = []

        for ticker in data:
            symbol = ticker['symbol']
            if symbol == self.ticker:
                tickers.append(ticker)

        if len(tickers) == 0:
            return None
        return tickers
    
    def main(self) -> list:
        data = self.get_binance_prices()
        info = self.find_ticker(data)
        return info