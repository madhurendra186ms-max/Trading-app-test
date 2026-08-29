import httpx

from config import SCORING_URL
from models import RankingResult


async def fetch_rankings(index: str, expiry: str) -> RankingResult:
    async with httpx.AsyncClient(timeout=2.0) as client:
        response = await client.get(
            f"{SCORING_URL}/v1/rankings", params={"index": index, "expiry": expiry}
        )
        response.raise_for_status()
    return RankingResult.model_validate(response.json())
