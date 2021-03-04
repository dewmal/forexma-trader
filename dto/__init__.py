from dataclasses import dataclass

from pydantic import BaseModel


class MarketStatus(BaseModel):
    asset: str
    unix: int
    date: str
    open: float
    high: float
    low: float
    close: float
    ask: float
    bid: float
    volume: float
