from fastapi import APIRouter, FastAPI, HTTPException, Request, status

from models import IndexVolume, MarketTick, ServiceHealth, StateSummary
from store import TickStore


def create_app() -> FastAPI:
    app = FastAPI(title="state-gateway", version="0.1.0")
    app.state.tick_store = TickStore()
    router = APIRouter(prefix="/v1", tags=["live state"])

    @app.get("/health", response_model=ServiceHealth, tags=["operations"])
    def health(request: Request) -> ServiceHealth:
        return ServiceHealth(service="state-gateway", status="ok")

    @router.post("/ticks", response_model=MarketTick, status_code=status.HTTP_201_CREATED)
    def upsert_tick(tick: MarketTick, request: Request) -> MarketTick:
        return request.app.state.tick_store.upsert(tick)

    @router.get("/ticks", response_model=list[MarketTick])
    def list_ticks(request: Request) -> list[MarketTick]:
        return list(request.app.state.tick_store.list())

    @router.get("/ticks/{instrument}", response_model=MarketTick)
    def get_tick(instrument: str, request: Request) -> MarketTick:
        tick = request.app.state.tick_store.get(instrument)
        if tick is None:
            raise HTTPException(status_code=404, detail="Instrument was not found")
        return tick

    @router.get("/state", response_model=StateSummary)
    def state_summary(request: Request) -> StateSummary:
        return StateSummary(instruments=request.app.state.tick_store.count())

    @router.get("/indexes/top-volume", response_model=list[IndexVolume])
    def top_indexes_by_volume(request: Request) -> list[IndexVolume]:
        return [
            IndexVolume(index=index, option_volume=option_volume)
            for index, option_volume in request.app.state.tick_store.top_indexes_by_volume(limit=5)
        ]

    app.include_router(router)
    return app


app = create_app()
