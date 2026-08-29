import httpx

from config import STATE_GATEWAY_URL
from models import MarketTick


async def fetch_ticks() -> list[MarketTick]:
    async with httpx.AsyncClient(timeout=2.0) as client:
        response = await client.get(f"{STATE_GATEWAY_URL}/v1/ticks")
        response.raise_for_status()
    return [MarketTick.model_validate(tick) for tick in response.json()]
