from enum import Enum

from pydantic import BaseModel, Field


class OptionType(str, Enum):
    CALL = "CE"
    PUT = "PE"


class ContractScore(BaseModel):
    instrument: str
    option_type: OptionType
    strike: float = Field(ge=0)
    ltp: float = Field(ge=0)
    score: float = Field(ge=0, le=100)


class RankingResult(BaseModel):
    index: str
    expiry: str
    rankings: list[ContractScore]


class PayoffScenario(BaseModel):
    underlying_at_expiry: float = Field(ge=0)
    payoff_points: float


class RiskProjection(BaseModel):
    instrument: str
    option_type: OptionType
    strike: float
    premium_points: float
    quantity: int = Field(gt=0)
    breakeven: float
    max_loss_points: float = Field(ge=0)
    max_profit_points: float | None
    reward_to_risk: float | None
    scenario: PayoffScenario | None
    unavailable_factors: list[str]
    assumptions: list[str]


class ServiceHealth(BaseModel):
    service: str
    status: str = "ok"
