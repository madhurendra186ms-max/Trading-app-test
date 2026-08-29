from fastapi import APIRouter, FastAPI

from models import MarketTick, OptionType, ServiceHealth

app = FastAPI(title="market-ingestion", version="0.1.0")
router = APIRouter(prefix="/v1", tags=["sample market data"])


@app.get("/health", response_model=ServiceHealth, tags=["operations"])
def health() -> ServiceHealth:
    return ServiceHealth(service="market-ingestion")


@router.get("/ticks", response_model=list[MarketTick])
def sample_ticks() -> list[MarketTick]:
    return [
        MarketTick(
            instrument="NFO:NIFTY26SEP24800CE",
            index="NIFTY 50",
            strike=24800,
            expiry="2026-09-04",
            option_type=OptionType.CALL,
            bid=132.45,
            ask=133.20,
            ltp=132.70,
            oi=25000000,
            volume=2170000,
            iv=12.8,
        ),
        MarketTick(
            instrument="NFO:NIFTY26SEP24800PE",
            index="NIFTY 50",
            strike=24800,
            expiry="2026-09-04",
            option_type=OptionType.PUT,
            bid=97.85,
            ask=98.40,
            ltp=98.10,
            oi=23500000,
            volume=2050000,
            iv=13.1,
        ),
    ]


app.include_router(router)
