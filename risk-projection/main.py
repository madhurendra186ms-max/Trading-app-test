import httpx
from fastapi import APIRouter, FastAPI, HTTPException, Query

from client import fetch_rankings
from engine import project_long_option
from models import RiskProjection, ServiceHealth

app = FastAPI(title="risk-projection", version="0.1.0")
router = APIRouter(prefix="/v1", tags=["risk projection"])


@app.get("/health", response_model=ServiceHealth, tags=["operations"])
def health() -> ServiceHealth:
    return ServiceHealth(service="risk-projection")


@router.get("/projections", response_model=RiskProjection)
async def projection(
    index: str = Query(min_length=1),
    expiry: str = Query(min_length=1),
    instrument: str = Query(min_length=1),
    quantity: int = Query(default=1, gt=0),
    underlying_at_expiry: float | None = Query(default=None, ge=0),
) -> RiskProjection:
    try:
        rankings = await fetch_rankings(index, expiry)
    except httpx.HTTPError as error:
        raise HTTPException(status_code=503, detail="Scoring service is unavailable") from error

    contract = next((item for item in rankings.rankings if item.instrument == instrument), None)
    if contract is None:
        raise HTTPException(status_code=404, detail="Instrument is not available in current rankings")
    return project_long_option(contract, quantity, underlying_at_expiry)


app.include_router(router)
