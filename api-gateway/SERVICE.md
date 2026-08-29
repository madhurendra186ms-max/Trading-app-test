# API Gateway Service

## Purpose
Provides the dashboard with a stable, browser-facing API that aggregates the live services. It does not store market or user data.

## Interface
- Port: `8009`
- Health: `GET /health`
- Dashboard: `GET /v1/dashboard?index={index}&expiry={expiry}`
- Projection: `GET /v1/projections?index={index}&expiry={expiry}&instrument={instrument}`
- Upstream: Option Chain (`8005`), Scoring (`8006`), Risk Projection (`8007`), Alerting (`8008`)
- Downstream: React Dashboard (planned, `8010`)
- API contract: `API.md`
- Service diagram: `SERVICE-DIAGRAM.md`

## Setup Log
| Step | Command | Verified result |
|---|---|---|
| 1 | port-listener check for `8009`; call Option Chain, Scoring, and Alerting APIs | Port `8009` was available; live APIs returned 1 chain row, 2 rankings, and 1 alert rule. |
| 2 | `Set-Location 'd:\Databricks\options-trading-app\api-gateway'; python -m venv .venv` | Created this service's private `.venv`. |
| 3 | `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt` | Installed FastAPI 0.141.1, Uvicorn 0.52.4, Pydantic 2.13.5, HTTPX 0.28.1, python-dotenv 1.2.3, and pytest 8.4.2. |
| 4 | `.\.venv\Scripts\python.exe -m pytest tests -q` | `2 passed in 0.86s`. |

## First Run
| Step | Command | Verified result |
|---|---|---|
| 1 | `Set-Location 'd:\Databricks\options-trading-app\api-gateway'; .\start.ps1` | Uvicorn started on `http://127.0.0.1:8009`. |
| 2 | `GET /health`, `GET /v1/dashboard`, and `GET /v1/projections` | Returned `api-gateway:ok`; dashboard had 1 chain row, 2 rankings, and 1 alert rule; proxy returned max loss `132.7` points. |

First independent run verified.

## Runbook
1. `Set-Location api-gateway`
2. `python -m venv .venv`
3. `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`
4. `.\start.ps1`
5. `Invoke-RestMethod http://127.0.0.1:8009/health`
6. `.\.venv\Scripts\python.exe -m pytest tests -q`

## Configuration
The service-local `.env` configures upstream service URLs and `DASHBOARD_ORIGIN`. It contains no credentials.

## Limits
- This MVP uses REST aggregation. Browser WebSocket fanout and rate limiting are later additions.
- User accounts and persistent watchlists/alerts are out of scope until persistent storage is added.
