import httpx
from fastapi import APIRouter, FastAPI, HTTPException, Query

from client import fetch_option_chain
from engine import rank_option_chain
from models import OptionType, RankingResult, ServiceHealth

app = FastAPI(title="scoring", version="0.1.0")
router = APIRouter(prefix="/v1", tags=["contract rankings"])


@app.get("/health", response_model=ServiceHealth, tags=["operations"])
def health() -> ServiceHealth:
    return ServiceHealth(service="scoring")


@router.get("/rankings", response_model=RankingResult)
async def rankings(
    index: str = Query(min_length=1),
    expiry: str = Query(min_length=1),
    option_type: OptionType | None = None,
) -> RankingResult:
    try:
        chain = await fetch_option_chain(index, expiry)
    except httpx.HTTPError as error:
        raise HTTPException(status_code=503, detail="Option Chain service is unavailable") from error

    return RankingResult(
        index=chain.index,
        expiry=chain.expiry,
        rankings=rank_option_chain(chain, option_type),
        unavailable_factors=["iv_rank", "momentum"],
    )


app.include_router(router)
