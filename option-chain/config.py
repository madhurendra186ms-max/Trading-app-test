import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))
STATE_GATEWAY_URL = os.getenv("STATE_GATEWAY_URL", "http://127.0.0.1:8003").rstrip("/")
