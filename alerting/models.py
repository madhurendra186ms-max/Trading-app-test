from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator


class OptionType(str, Enum):
    CALL = "CE"
    PUT = "PE"


class ContractScore(BaseModel):
    instrument: str
    option_type: OptionType
    strike: float
    ltp: float
    spread_percent: float
    score: float


class RankingResult(BaseModel):
    index: str
    expiry: str
    rankings: list[ContractScore]


class AlertRuleCreate(BaseModel):
    index: str = Field(min_length=1)
    expiry: str = Field(min_length=1)
    option_type: OptionType | None = None
    min_score: float | None = Field(default=None, ge=0, le=100)
    max_spread_percent: float | None = Field(default=None, ge=0)
    cooldown_seconds: int = Field(default=60, ge=0)

    @model_validator(mode="after")
    def has_condition(self) -> "AlertRuleCreate":
        if self.min_score is None and self.max_spread_percent is None:
            raise ValueError("At least one alert condition is required")
        return self


class AlertRule(AlertRuleCreate):
    id: str = Field(default_factory=lambda: str(uuid4()))


class AlertEvent(BaseModel):
    rule_id: str
    instrument: str
    score: float
    spread_percent: float
    triggered_at: datetime


class EvaluationResult(BaseModel):
    triggered: list[AlertEvent]


class ServiceHealth(BaseModel):
    service: str
    status: str = "ok"
