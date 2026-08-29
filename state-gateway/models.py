from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class OptionType(str, Enum):
    CALL = "CE"
    PUT = "PE"


class MarketTick(BaseModel):
    instrument: str = Field(min_length=1)
    index: str = Field(min_length=1)
    strike: float = Field(ge=0)
    expiry: str = Field(min_length=1)
    option_type: OptionType
    bid: float = Field(ge=0)
    ask: float = Field(ge=0)
    ltp: float = Field(ge=0)
    oi: int = Field(ge=0)
    volume: int = Field(ge=0)
    iv: float = Field(ge=0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ServiceHealth(BaseModel):
    service: str
    status: str = "ok"


class StateSummary(BaseModel):
    instruments: int = Field(ge=0)


class IndexVolume(BaseModel):
    index: str
    option_volume: int = Field(ge=0)


__all__ = ["IndexVolume", "MarketTick", "OptionType", "ServiceHealth", "StateSummary"]
