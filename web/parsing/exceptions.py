class BaseError(Exception):
    """Базовый класс для ошибок."""
    pass


class MissingSpotTradingAllowError(BaseError):
    """
    Ошибка отсутствия параметра spot_trading_allow.
    """
    def __init__(self, message="Missing spot_trading_allow dict"):
        self.message = message
        super().__init__(self.message)


class MissingSpotPricesError(BaseError):
    """
    Ошибка отсутствия спотовых цен.
    """
    def __init__(self, message="Missing spot_prices list"):
        self.message = message
        super().__init__(self.message)

