from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from kiteconnect import KiteConnect
from kiteconnect.exceptions import KiteException

from config import load_kite_settings
from models import KiteAuthResult, MarketTick, OptionType, ServiceHealth

app = FastAPI(title="market-ingestion", version="0.1.0")
app.state.kite_settings = load_kite_settings()
router = APIRouter(prefix="/v1", tags=["sample market data"])


@app.get("/health", response_model=ServiceHealth, tags=["operations"])
def health() -> ServiceHealth:
    return ServiceHealth(service="market-ingestion")


@router.get("/auth/kite/login", status_code=307, tags=["kite authentication"])
def kite_login() -> RedirectResponse:
    settings = app.state.kite_settings
    if not settings.api_key:
        raise HTTPException(status_code=503, detail="KITE_API_KEY is not configured")

    return RedirectResponse(url=KiteConnect(api_key=settings.api_key).login_url())


@router.get("/auth/kite/callback", response_model=KiteAuthResult, tags=["kite authentication"])
def kite_callback(request_token: str, status: str = "success") -> KiteAuthResult:
    settings = app.state.kite_settings
    if status != "success":
        raise HTTPException(status_code=400, detail="Kite login was not successful")
    if not settings.api_key or not settings.api_secret:
        raise HTTPException(status_code=503, detail="Kite API configuration is incomplete")

    try:
        kite = KiteConnect(api_key=settings.api_key)
        session = kite.generate_session(request_token, api_secret=settings.api_secret)
        access_token = session["access_token"]
    except (KiteException, KeyError) as error:
        raise HTTPException(status_code=502, detail="Unable to establish Kite session") from error

    kite.set_access_token(access_token)
    app.state.kite_client = kite
    app.state.kite_access_token = access_token
    return KiteAuthResult(authenticated=True, message="Kite session established")


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
