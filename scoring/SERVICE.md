# Scoring Service

## Purpose
Ranks option contracts by live liquidity. This is decision support, not a buy/sell signal or profit guarantee.

## Interface
- Port: `8006`
- Health: `GET /health`
- Rankings: `GET /v1/rankings?index={index}&expiry={expiry}&option_type={CE|PE}`
- Upstream: Option Chain (`8005`)
- Downstream: Risk Projection, Alerting, and API Gateway (planned)
- API contract: `API.md`
- Service diagram: `SERVICE-DIAGRAM.md`

## Setup Log
| Step | Command | Verified result |
|---|---|---|
| 1 | port-listener check for `8006`; `GET` current Option Chain | Port `8006` was available; Option Chain returned 1 row with both CE and PE. |
| 2 | `Set-Location 'd:\Databricks\options-trading-app\scoring'; python -m venv .venv` | Created this service's private `.venv`. |
| 3 | `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt` | Installed FastAPI 0.141.1, Uvicorn 0.52.4, Pydantic 2.13.5, HTTPX 0.28.1, python-dotenv 1.2.3, and pytest 8.4.2. |
| 4 | `.\.venv\Scripts\python.exe -m pytest tests -q` | `3 passed in 0.36s`. |

## First Run
| Step | Command | Verified result |
|---|---|---|
| 1 | `Set-Location 'd:\Databricks\options-trading-app\scoring'; .\start.ps1` | Uvicorn started on `http://127.0.0.1:8006`. |
| 2 | `GET /health` and CE-filtered `GET /v1/rankings` | Returned `scoring:ok`; 1 CE ranking for `NFO:NIFTY26SEP24800CE` with score `94.37`; unavailable factors were `iv_rank,momentum`. |

First independent run verified.

## Runbook
1. `Set-Location scoring`
2. `python -m venv .venv`
3. `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`
4. `.\start.ps1`
5. `Invoke-RestMethod http://127.0.0.1:8006/health`
6. `.\.venv\Scripts\python.exe -m pytest tests -q`

## Scoring Model
- Spread: up to 40 points; tighter percentage spread scores higher.
- Volume: up to 30 points; reaches the cap at 2,000,000 contracts.
- Open interest: up to 30 points; reaches the cap at 25,000,000 contracts.
- IV rank and momentum: unavailable until the application collects historical observations.

## Configuration
`OPTION_CHAIN_URL` is loaded from this service's `.env` and defaults to
`http://127.0.0.1:8005`.
