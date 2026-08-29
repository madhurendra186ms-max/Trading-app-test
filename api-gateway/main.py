import asyncio
from typing import Any

import httpx
from fastapi import APIRouter, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from client import fetch_option_chain, fetch_projection, fetch_rankings, fetch_rules
from config import DASHBOARD_ORIGIN
from models import DashboardOverview, ServiceHealth

app = FastAPI(title="api-gateway", version="0.1.0")
allowed_origins = [DASHBOARD_ORIGIN]
if "127.0.0.1" in DASHBOARD_ORIGIN:
    allowed_origins.append(DASHBOARD_ORIGIN.replace("127.0.0.1", "localhost"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=[],
)
router = APIRouter(prefix="/v1", tags=["dashboard"])


@app.get("/health", response_model=ServiceHealth, tags=["operations"])
def health() -> ServiceHealth:
    return ServiceHealth(service="api-gateway")


@router.get("/dashboard", response_model=DashboardOverview)
async def dashboard(index: str = Query(min_length=1), expiry: str = Query(min_length=1)) -> DashboardOverview:
    try:
        option_chain, rankings, rules = await asyncio.gather(
            fetch_option_chain(index, expiry), fetch_rankings(index, expiry), fetch_rules()
        )
    except httpx.HTTPError as error:
        raise HTTPException(status_code=503, detail="A live data service is unavailable") from error
    return DashboardOverview(
        index=index,
        expiry=expiry,
        option_chain=option_chain,
        rankings=rankings,
        active_alert_rules=len(rules),
    )


@router.get("/projections")
async def projection(
    index: str = Query(min_length=1),
    expiry: str = Query(min_length=1),
    instrument: str = Query(min_length=1),
    quantity: int = Query(default=1, gt=0),
    underlying_at_expiry: float | None = Query(default=None, ge=0),
) -> dict[str, Any]:
    params: dict[str, Any] = {
        "index": index,
        "expiry": expiry,
        "instrument": instrument,
        "quantity": quantity,
    }
    if underlying_at_expiry is not None:
        params["underlying_at_expiry"] = underlying_at_expiry
    try:
        return await fetch_projection(params)
    except httpx.HTTPStatusError as error:
        raise HTTPException(status_code=error.response.status_code, detail="Projection request failed") from error
    except httpx.HTTPError as error:
        raise HTTPException(status_code=503, detail="Risk Projection service is unavailable") from error


app.include_router(router)
