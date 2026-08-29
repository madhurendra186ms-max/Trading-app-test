import httpx

from config import OPTION_CHAIN_URL
from models import OptionChain


async def fetch_option_chain(index: str, expiry: str) -> OptionChain:
    async with httpx.AsyncClient(timeout=2.0) as client:
        response = await client.get(
            f"{OPTION_CHAIN_URL}/v1/option-chain", params={"index": index, "expiry": expiry}
        )
        response.raise_for_status()
    return OptionChain.model_validate(response.json())
