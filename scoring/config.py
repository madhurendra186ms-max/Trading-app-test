import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))
OPTION_CHAIN_URL = os.getenv("OPTION_CHAIN_URL", "http://127.0.0.1:8005").rstrip("/")
