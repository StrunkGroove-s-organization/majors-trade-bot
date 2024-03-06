from parsing.exceptions import BaseError


class MissingPositiveLinksError(BaseError):
    def __init__(self, message="Missing positive_links"):
        self.message = message
        super().__init__(self.message)


class MissingProfitLinksrror(BaseError):
    def __init__(self, message="Missing profit_links"):
        self.message = message
        super().__init__(self.message)

