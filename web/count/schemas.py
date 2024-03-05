from pydantic import BaseModel
from parsing.schemas import DataBookTicker


class ProfitLink(BaseModel):
    first: DataBookTicker
    second: DataBookTicker
    third: DataBookTicker
    spread: float
