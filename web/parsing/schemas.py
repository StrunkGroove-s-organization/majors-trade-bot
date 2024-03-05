from pydantic import BaseModel, validator
    

class SymbolInfo(BaseModel):
    base: str
    quote: str


class DataBookTicker(BaseModel):
    base: str
    quote: str
    bid_price: float
    bid_qty: float
    ask_price: float
    ask_qty: float
    fake: bool = False
    
    @property
    def symbol(self) -> str:
        return self.base + self.quote