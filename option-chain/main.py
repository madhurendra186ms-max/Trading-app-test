import httpx
from fastapi import APIRouter, FastAPI, HTTPException, Query

from chain import build_option_chain, list_expiries
from client import fetch_ticks
from models import ExpiryList, OptionChain, ServiceHealth

app = FastAPI(title="option-chain", version="0.1.0")
router = APIRouter(prefix="/v1", tags=["option chain"])


@app.get("/health", response_model=ServiceHealth, tags=["operations"])
def health() -> ServiceHealth:
    return ServiceHealth(service="option-chain")


async def current_ticks():
    try:
        return await fetch_ticks()
    except httpx.HTTPError as error:
        raise HTTPException(status_code=503, detail="State Gateway is unavailable") from error


@router.get("/option-chain", response_model=OptionChain)
async def option_chain(
    index: str = Query(min_length=1), expiry: str = Query(min_length=1)
) -> OptionChain:
    return build_option_chain(await current_ticks(), index, expiry)


@router.get("/option-chain/expiries", response_model=ExpiryList)
async def expiries(index: str = Query(min_length=1)) -> ExpiryList:
    return ExpiryList(index=index, expiries=list_expiries(await current_ticks(), index))


app.include_router(router)
