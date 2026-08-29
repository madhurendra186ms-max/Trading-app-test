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


class ScoreComponents(BaseModel):
    spread: float = Field(ge=0, le=40)
    volume: float = Field(ge=0, le=30)
    open_interest: float = Field(ge=0, le=30)


class ContractScore(BaseModel):
    instrument: str
    option_type: OptionType
    strike: float
    ltp: float
    spread_percent: float = Field(ge=0)
    score: float = Field(ge=0, le=100)
    components: ScoreComponents


class RankingResult(BaseModel):
    index: str
    expiry: str
    rankings: list[ContractScore]
    unavailable_factors: list[str]


class ServiceHealth(BaseModel):
    service: str
    status: str = "ok"
