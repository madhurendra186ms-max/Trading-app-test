# Option Chain Service

## Purpose
Reads normalized live ticks from State Gateway and pairs CE/PE contracts by index, expiry, and strike.

## Interface
- Port: `8005`
- Health: `GET /health`
- Chain: `GET /v1/option-chain?index={index}&expiry={expiry}`
- Expiries: `GET /v1/option-chain/expiries?index={index}`
- Upstream: State Gateway (`8003`)
- Downstream: Scoring and API Gateway (planned)
- API contract: `API.md`
- Service diagram: `SERVICE-DIAGRAM.md`

## Setup Log
| Step | Command | Verified result |
|---|---|---|
| 1 | port-listener check for `8005`; `GET http://127.0.0.1:8003/v1/ticks` | Port `8005` was available; State Gateway returned 1 tick. |
| 2 | `Set-Location 'd:\Databricks\options-trading-app\option-chain'; python -m venv .venv` | Created this service's private `.venv`. |
| 3 | `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt` | Installed FastAPI 0.141.1, Uvicorn 0.52.4, Pydantic 2.13.5, HTTPX 0.28.1, python-dotenv 1.2.3, and pytest 8.4.2. |
| 4 | `.\.venv\Scripts\python.exe -m pytest tests -q` | `3 passed in 0.48s`. |

## First Run
| Step | Command | Verified result |
|---|---|---|
| 1 | `Set-Location 'd:\Databricks\options-trading-app\option-chain'; .\start.ps1` | Uvicorn started on `http://127.0.0.1:8005`. |
| 2 | `POST` a NIFTY PE tick to State Gateway, then call the Option Chain APIs | Health returned `option-chain:ok`; chain returned 1 row with paired `NFO:NIFTY26SEP24800CE` and `NFO:NIFTY26SEP24800PE`; expiry was `2026-09-04`. |

First independent run verified.

## Runbook
1. `Set-Location option-chain`
2. `python -m venv .venv`
3. `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`
4. `.\start.ps1`
5. `Invoke-RestMethod http://127.0.0.1:8005/health`
6. `.\.venv\Scripts\python.exe -m pytest tests -q`

## Configuration
`STATE_GATEWAY_URL` is loaded from the service-local `.env` file. It defaults to
`http://127.0.0.1:8003` and contains no secrets.
