import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))


@dataclass(frozen=True)
class KiteSettings:
    api_key: str
    api_secret: str
    access_token: str
    redirect_url: str


def load_kite_settings() -> KiteSettings:
    return KiteSettings(
        api_key=os.getenv("KITE_API_KEY", ""),
        api_secret=os.getenv("KITE_API_SECRET", ""),
        access_token=os.getenv("KITE_ACCESS_TOKEN", ""),
        redirect_url=os.getenv("KITE_REDIRECT_URL", ""),
    )
