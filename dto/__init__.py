from pydantic import BaseModel
from pydantic.class_validators import validator


class MarketStatus(BaseModel):
    asset: str
    interval: str
    unix: int
    date: int
    open: float
    high: float
    low: float
    close: float
    ask: float
    bid: float
    volume: float

    @validator('high')
    def high_is_higher_than_others(cls, v, values, **kwargs):
        if 'close' in values and 'low' in values and 'open' in values:
            if v > values['close'] and v >= values['open'] and v >= values['low']:
                raise ValueError('high must be higher than others')
        return v


class TechnicalAnalysisSnapshot(BaseModel):
    name: str
    unix: int
    date: int
    values: dict


class Order(BaseModel):
    id: str
    unix: int
    date: int
