from typing import Any

import httpx

from config import ALERTING_URL, OPTION_CHAIN_URL, RISK_PROJECTION_URL, SCORING_URL


async def get_json(url: str, params: dict[str, Any] | None = None) -> Any:
    async with httpx.AsyncClient(timeout=2.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
    return response.json()


async def fetch_option_chain(index: str, expiry: str) -> dict[str, Any]:
    return await get_json(f"{OPTION_CHAIN_URL}/v1/option-chain", {"index": index, "expiry": expiry})


async def fetch_rankings(index: str, expiry: str) -> dict[str, Any]:
    return await get_json(f"{SCORING_URL}/v1/rankings", {"index": index, "expiry": expiry})


async def fetch_rules() -> list[dict[str, Any]]:
    return await get_json(f"{ALERTING_URL}/v1/rules")


async def fetch_projection(params: dict[str, Any]) -> dict[str, Any]:
    return await get_json(f"{RISK_PROJECTION_URL}/v1/projections", params)
