import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))
OPTION_CHAIN_URL = os.getenv("OPTION_CHAIN_URL", "http://127.0.0.1:8005").rstrip("/")
SCORING_URL = os.getenv("SCORING_URL", "http://127.0.0.1:8006").rstrip("/")
RISK_PROJECTION_URL = os.getenv("RISK_PROJECTION_URL", "http://127.0.0.1:8007").rstrip("/")
ALERTING_URL = os.getenv("ALERTING_URL", "http://127.0.0.1:8008").rstrip("/")
DASHBOARD_ORIGIN = os.getenv("DASHBOARD_ORIGIN", "http://127.0.0.1:8010")
