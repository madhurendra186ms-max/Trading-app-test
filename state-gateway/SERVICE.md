# State Gateway Service

## Purpose
Owns the latest live market tick for each instrument during a single application session.
It starts without a database; Redis is added only for multi-process state or restart recovery.

## Interface
- Port: `8003`
- Health: `GET /health`
- Inbound API: `POST /v1/ticks`
- Read API: `GET /v1/ticks`, `GET /v1/ticks/{instrument}`, `GET /v1/state`
- Upstream: Market Ingestion Service (`8002`)
- Downstream: Option Chain Service (`8005`) and Scoring Service (`8006`)
- API contract: `API.md`
- Service diagram: `SERVICE-DIAGRAM.md`

## Setup Log
| Step | Command | Verified result |
|---|---|---|
| 1 | port-listener check for `8003` | No active listener was returned before service setup. |
| 2 | `Set-Location 'd:\Databricks\options-trading-app\state-gateway'; python -m venv .venv` | Created this service's private `.venv`. |
| 3 | `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt` | Installed FastAPI 0.141.1, Uvicorn 0.52.4, Pydantic 2.13.5, HTTPX 0.28.1, and pytest 8.4.2. |
| 4 | `.\.venv\Scripts\python.exe -m pytest tests -q` | `3 passed in 0.77s`. |
| 5 | Received first `GET /v1/ticks` item from Market Ingestion through `POST /v1/ticks` | Stored `NFO:NIFTY26SEP24800CE`; `GET /v1/ticks` returned 1 current tick. |

## First Run
| Step | Command | Verified result |
|---|---|---|
| 1 | `Set-Location 'd:\Databricks\options-trading-app\state-gateway'; .\start.ps1` | Uvicorn started on `http://127.0.0.1:8003`. |
| 2 | `POST /v1/ticks`, then `GET /v1/state` and `GET /v1/ticks/{instrument}` | Returned `state-gateway:ok`; stored `NFO:NIFTY26SEP24800CE`; count was `1`; LTP was `132.7`. |

First independent run verified.

## Runbook
1. `Set-Location state-gateway`
2. `python -m venv .venv`
3. `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`
4. `.\start.ps1`
5. `Invoke-RestMethod http://127.0.0.1:8003/health`
6. `.\.venv\Scripts\python.exe -m pytest tests -q`

## Storage Model
The process holds state in memory. Restarting the service clears all ticks. Each instrument has
one current tick; an older timestamp cannot replace a newer stored tick.
