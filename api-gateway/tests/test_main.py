import httpx
import pytest

import main
from main import app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_dashboard_aggregates_live_service_shapes(monkeypatch: pytest.MonkeyPatch) -> None:
    async def option_chain(index: str, expiry: str) -> dict[str, object]:
        return {"index": index, "expiry": expiry, "rows": []}

    async def rankings(index: str, expiry: str) -> dict[str, object]:
        return {"index": index, "expiry": expiry, "rankings": []}

    async def rules() -> list[dict[str, object]]:
        return [{"id": "rule-1"}]

    monkeypatch.setattr(main, "fetch_option_chain", option_chain)
    monkeypatch.setattr(main, "fetch_rankings", rankings)
    monkeypatch.setattr(main, "fetch_rules", rules)
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/dashboard", params={"index": "NIFTY 50", "expiry": "2026-09-04"})

    assert response.status_code == 200
    assert response.json()["active_alert_rules"] == 1
    assert response.json()["option_chain"]["index"] == "NIFTY 50"


@pytest.mark.anyio
async def test_projection_forwards_all_request_parameters(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    async def projection(params: dict[str, object]) -> dict[str, object]:
        captured.update(params)
        return {"instrument": params["instrument"], "max_loss_points": 100.0}

    monkeypatch.setattr(main, "fetch_projection", projection)
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/v1/projections",
            params={
                "index": "NIFTY 50",
                "expiry": "2026-09-04",
                "instrument": "NFO:NIFTY26SEP24800CE",
                "quantity": 2,
                "underlying_at_expiry": 25000,
            },
        )

    assert response.status_code == 200
    assert captured["quantity"] == 2
    assert captured["underlying_at_expiry"] == 25000.0


@pytest.mark.anyio
async def test_dashboard_localhost_origin_is_allowed() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.options(
            "/v1/dashboard",
            headers={
                "Origin": "http://localhost:8010",
                "Access-Control-Request-Method": "GET",
            },
        )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:8010"
