# Market Ingestion Service

## Purpose
Provides normalized option ticks. It returns deterministic sample data until the Zerodha Kite
Connect adapter is configured.

## Interface
- Port: `8002`
- Health: `GET /health`
- Sample ticks: `GET /v1/ticks`
- Dependencies: local Python environment, FastAPI; no database or external service for MVP.
- Downstream consumer: Option Chain Service (`8005`).

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
