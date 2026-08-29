import httpx
import pytest

import main
from main import app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_sample_ticks_match_the_normalized_option_contract() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/ticks")

    assert response.status_code == 200
    ticks = response.json()
    assert len(ticks) == 2
    assert ticks[0]["option_type"] == "CE"
    assert ticks[1]["option_type"] == "PE"
    assert ticks[0]["bid"] < ticks[0]["ask"]


@pytest.mark.anyio
async def test_kite_login_redirects_to_kite_authorization() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/auth/kite/login", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"].startswith("https://kite.zerodha.com/connect/login?")
    assert "api_key=" in response.headers["location"]


@pytest.mark.anyio
async def test_kite_callback_stores_the_session_token_only_in_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeKiteConnect:
        def __init__(self, api_key: str) -> None:
            self.api_key = api_key
            self.access_token = ""

        def generate_session(self, request_token: str, api_secret: str) -> dict[str, str]:
            assert request_token == "one-time-token"
            assert api_secret
            return {"access_token": "daily-token"}

        def set_access_token(self, access_token: str) -> None:
            self.access_token = access_token

    monkeypatch.setattr(main, "KiteConnect", FakeKiteConnect)
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/v1/auth/kite/callback",
            params={"status": "success", "request_token": "one-time-token"},
        )

    assert response.status_code == 200
    assert response.json() == {"authenticated": True, "message": "Kite session established"}
    assert app.state.kite_access_token == "daily-token"
