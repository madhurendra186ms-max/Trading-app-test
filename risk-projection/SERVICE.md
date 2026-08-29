# Risk Projection Service

## Purpose
Calculates transparent payoff and risk values for a long option position. It does not predict or guarantee profit.

## Interface
- Port: `8007`
- Health: `GET /health`
- Projection: `GET /v1/projections?index={index}&expiry={expiry}&instrument={instrument}`
- Upstream: Scoring (`8006`)
- Downstream: Alerting and API Gateway (planned)
- API contract: `API.md`
- Service diagram: `SERVICE-DIAGRAM.md`

## Setup Log
| Step | Command | Verified result |
|---|---|---|
| 1 | port-listener check for `8007`; `GET` current Scoring rankings | Port `8007` was available; Scoring returned 2 ranked contracts. |
| 2 | `Set-Location 'd:\Databricks\options-trading-app\risk-projection'; python -m venv .venv` | Created this service's private `.venv`. |
| 3 | `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt` | Installed FastAPI 0.141.1, Uvicorn 0.52.4, Pydantic 2.13.5, HTTPX 0.28.1, python-dotenv 1.2.3, and pytest 8.4.2. |
| 4 | `.\.venv\Scripts\python.exe -m pytest tests -q` | `3 passed in 0.32s`. |

## First Run
| Step | Command | Verified result |
|---|---|---|
| 1 | `Set-Location 'd:\Databricks\options-trading-app\risk-projection'; .\start.ps1` | Uvicorn started on `http://127.0.0.1:8007`. |
| 2 | `GET /health` and a CE `GET /v1/projections` scenario | Returned `risk-projection:ok`; breakeven `24932.7`, max loss `132.7` points, payoff `67.3` points, and unavailable factor `probability_of_profit`. |

First independent run verified.

## Runbook
1. `Set-Location risk-projection`
2. `python -m venv .venv`
3. `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`
4. `.\start.ps1`
5. `Invoke-RestMethod http://127.0.0.1:8007/health`
6. `.\.venv\Scripts\python.exe -m pytest tests -q`

## Units and Limits
- All values are in option premium points multiplied by `quantity`.
- Rupee values require an explicit current lot-size source and broker charges, neither of which is added yet.
- Probability of profit requires historical data and is reported as unavailable.

## Configuration
`SCORING_URL` is loaded from this service's `.env` and defaults to `http://127.0.0.1:8006`.
