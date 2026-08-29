import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))
SCORING_URL = os.getenv("SCORING_URL", "http://127.0.0.1:8006").rstrip("/")
