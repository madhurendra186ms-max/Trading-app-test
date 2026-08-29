from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class OptionType(str, Enum):
    CALL = "CE"
    PUT = "PE"


class MarketTick(BaseModel):
    instrument: str
    index: str
    strike: float
    expiry: str
    option_type: OptionType
    bid: float = Field(ge=0)
    ask: float = Field(ge=0)
    ltp: float = Field(ge=0)
    oi: int = Field(ge=0)
    volume: int = Field(ge=0)
    iv: float = Field(ge=0)
    timestamp: datetime


class ChainRow(BaseModel):
    strike: float
    call: MarketTick | None = None
    put: MarketTick | None = None


class OptionChain(BaseModel):
    index: str
    expiry: str
    rows: list[ChainRow]


class ExpiryList(BaseModel):
    index: str
    expiries: list[str]


class ServiceHealth(BaseModel):
    service: str
    status: str = "ok"
