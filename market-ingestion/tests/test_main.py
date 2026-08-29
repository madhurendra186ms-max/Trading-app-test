import httpx
import pytest

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
