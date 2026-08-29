from typing import Any

from pydantic import BaseModel, Field


class DashboardOverview(BaseModel):
    index: str
    expiry: str
    option_chain: dict[str, Any]
    rankings: dict[str, Any]
    active_alert_rules: int = Field(ge=0)


class ServiceHealth(BaseModel):
    service: str
    status: str = "ok"
