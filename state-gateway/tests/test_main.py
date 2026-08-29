from datetime import datetime, timedelta, timezone

import httpx
import pytest

from main import create_app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def app_client() -> tuple[httpx.AsyncClient, httpx.ASGITransport]:
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    return httpx.AsyncClient(transport=transport, base_url="http://test"), transport


def tick_payload(timestamp: datetime) -> dict[str, object]:
    return {
        "instrument": "NFO:NIFTY26SEP24800CE",
        "index": "NIFTY 50",
        "strike": 24800,
        "expiry": "2026-09-04",
        "option_type": "CE",
        "bid": 132.45,
        "ask": 133.20,
        "ltp": 132.70,
        "oi": 25000000,
        "volume": 2170000,
        "iv": 12.8,
        "timestamp": timestamp.isoformat(),
    }


@pytest.mark.anyio
async def test_posted_tick_can_be_retrieved_and_counted(app_client: tuple[httpx.AsyncClient, httpx.ASGITransport]) -> None:
    client, _ = app_client
    async with client:
        timestamp = datetime.now(timezone.utc)
        create_response = await client.post("/v1/ticks", json=tick_payload(timestamp))
        get_response = await client.get("/v1/ticks/NFO:NIFTY26SEP24800CE")
        summary_response = await client.get("/v1/state")

    assert create_response.status_code == 201
    assert get_response.status_code == 200
    assert get_response.json()["instrument"] == "NFO:NIFTY26SEP24800CE"
    assert summary_response.json() == {"instruments": 1}


@pytest.mark.anyio
async def test_older_tick_cannot_replace_newer_state(app_client: tuple[httpx.AsyncClient, httpx.ASGITransport]) -> None:
    client, _ = app_client
    async with client:
        newest = datetime.now(timezone.utc)
        older = newest - timedelta(seconds=1)
        newest_payload = tick_payload(newest)
        older_payload = tick_payload(older)
        newest_payload["ltp"] = 140.0
        older_payload["ltp"] = 120.0
        await client.post("/v1/ticks", json=newest_payload)
        response = await client.post("/v1/ticks", json=older_payload)

    assert response.status_code == 201
    assert response.json()["ltp"] == 140.0


@pytest.mark.anyio
async def test_unknown_instrument_returns_not_found(app_client: tuple[httpx.AsyncClient, httpx.ASGITransport]) -> None:
    client, _ = app_client
    async with client:
        response = await client.get("/v1/ticks/NFO:UNKNOWN")

    assert response.status_code == 404
    assert response.json() == {"detail": "Instrument was not found"}


@pytest.mark.anyio
async def test_top_indexes_are_ranked_by_total_current_option_volume(app_client: tuple[httpx.AsyncClient, httpx.ASGITransport]) -> None:
    client, _ = app_client
    async with client:
        nifty = tick_payload(datetime.now(timezone.utc))
        bank_nifty = tick_payload(datetime.now(timezone.utc))
        bank_nifty["instrument"] = "NFO:BANKNIFTY26SEP56000CE"
        bank_nifty["index"] = "BANK NIFTY"
        bank_nifty["volume"] = 3_000_000
        await client.post("/v1/ticks", json=nifty)
        await client.post("/v1/ticks", json=bank_nifty)
        response = await client.get("/v1/indexes/top-volume")

    assert response.status_code == 200
    assert response.json()[0] == {"index": "BANK NIFTY", "option_volume": 3_000_000}
