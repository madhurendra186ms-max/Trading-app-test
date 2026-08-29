# Market Ingestion Service

## Purpose
Provides normalized option ticks. It returns deterministic sample data until the Zerodha Kite
Connect adapter is configured.

## Interface
- Port: `8002`
- Health: `GET /health`
- Sample ticks: `GET /v1/ticks`
- Kite login: `GET /v1/auth/kite/login`
- Kite callback: `GET /v1/auth/kite/callback`
- Dependencies: local Python environment, FastAPI; no database or external service for MVP.
- Downstream consumer: Option Chain Service (`8005`).
- API contract: `API.md`

## Setup Log
| Step | Command | Verified result |
|---|---|---|
| 1 | `python --version` | `Python 3.14.3` available on the machine. |
| 2 | `node --version` | `v22.22.0` available on the machine. |
| 3 | `npm --version` | `11.17.0` available on the machine. |
| 4 | port-listener check for `8001..8011` | No active listener was returned before service setup. |
| 5 | `Set-Location 'd:\Databricks\options-trading-app\market-ingestion'; python -m venv .venv` | Created this service's private `.venv`. |
| 6 | `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt` | Installed FastAPI 0.141.1, Uvicorn 0.52.4, Pydantic 2.13.5, HTTPX 0.28.1, and pytest 8.4.2. |
| 7 | `.\.venv\Scripts\python.exe -m pytest tests -q` | `1 passed in 0.62s`. |
| 8 | `Remove-Item -Recurse -Force .\services\market_ingestion` | Removed the obsolete duplicate after the isolated service was verified. |
| 9 | `Test-Path .\services\market_ingestion; Invoke-RestMethod http://127.0.0.1:8002/health` | `legacy_exists=False`; service returned `market-ingestion:ok`. |
| 10 | `Remove-Item -Recurse -Force .\.venv, .\.pytest_cache, .\scripts, .\shared, .\services; Remove-Item -Force .\.gitignore, .\requirements.txt, .\requirements-dev.txt` | Removed obsolete root runtime, shared code, and placeholder services after Module 2 became self-contained. |
| 11 | `Get-ChildItem -File -Force; Invoke-RestMethod http://127.0.0.1:8002/health` | Root file list contains only `README.md`; service returned `market-ingestion:ok`. |
| 12 | `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt; .\.venv\Scripts\python.exe -m pytest tests -q` | `python-dotenv` installed; `1 passed in 0.55s`. |
| 13 | `.\.venv\Scripts\python.exe -c "from config import load_kite_settings; ..."` | Loaded configured redirect URL; API key, secret, and access token were blank and not displayed. |
| 14 | PowerShell `HttpClient` redirect check | Did not run because the session had not loaded the `System.Net.Http` assembly. |
| 15 | `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt; .\.venv\Scripts\python.exe -m pytest tests -q` | Installed `kiteconnect`; `2 passed in 1.42s`. |
| 16 | `Add-Type -AssemblyName System.Net.Http; ... GET /v1/auth/kite/login` | Returned `307`; redirect host was `kite.zerodha.com` without displaying query data. |
| 17 | `.\.venv\Scripts\python.exe -m pytest tests -q; .\.venv\Scripts\python.exe -m compileall -q main.py models.py config.py` | `3 passed in 1.05s`; callback exchange behavior is validated with a fake Kite client. |
| 18 | `Invoke-RestMethod http://127.0.0.1:8002/openapi.json` | Live schema contains `/v1/auth/kite/callback`. |
| 19 | `Invoke-WebRequest http://127.0.0.1:8002/v1/auth/kite/callback` without query data | Returned `422`, confirming the live route is active and requires `request_token`. |

## First Run
| Step | Command | Verified result |
|---|---|---|
| 1 | `Set-Location 'd:\Databricks\options-trading-app\market-ingestion'; .\start.ps1` | Uvicorn started on `http://127.0.0.1:8002`. |
| 2 | `Invoke-RestMethod http://127.0.0.1:8002/health` | Returned `market-ingestion:ok`. |
| 3 | `Invoke-RestMethod http://127.0.0.1:8002/v1/ticks` | Returned 2 ticks; first instrument was `NFO:NIFTY26SEP24800CE`. |

First independent run verified.

## Runbook
1. `Set-Location market-ingestion`
2. `python -m venv .venv`
3. `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`
4. `.\start.ps1`
5. `Invoke-RestMethod http://127.0.0.1:8002/health`
6. `.\.venv\Scripts\python.exe -m pytest tests -q`

## Configuration
Future Kite configuration uses `KITE_API_KEY`, `KITE_API_SECRET`, and `KITE_ACCESS_TOKEN`.
Do not record credential values in this file.

The service loads `.env` from this folder at startup. The local `.env` is ignored by Git;
fill in its values locally when Kite Connect is ready.
