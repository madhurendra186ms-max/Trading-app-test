# Alerting Service

## Purpose
Maintains session-only alert rules and evaluates them against current Scoring rankings. It does not place trades or guarantee outcomes.

## Interface
- Port: `8008`
- Health: `GET /health`
- Create rule: `POST /v1/rules`
- List rules: `GET /v1/rules`
- Evaluate rules: `POST /v1/evaluate`
- Upstream: Scoring (`8006`)
- Downstream: API Gateway (planned)
- API contract: `API.md`
- Service diagram: `SERVICE-DIAGRAM.md`

## Setup Log
| Step | Command | Verified result |
|---|---|---|
| 1 | port-listener check for `8008`; `GET` current Scoring rankings | Port `8008` was available; Scoring returned 2 rankings with score and spread fields. |
| 2 | `Set-Location 'd:\Databricks\options-trading-app\alerting'; python -m venv .venv` | Created this service's private `.venv`. |
| 3 | `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt` | Installed FastAPI 0.141.1, Uvicorn 0.52.4, Pydantic 2.13.5, HTTPX 0.28.1, python-dotenv 1.2.3, and pytest 8.4.2. |
| 4 | `.\.venv\Scripts\python.exe -m pytest tests -q` | `3 passed in 0.31s`. |
| 5 | `POST /v1/rules` live verification | Failed with `500`; Pydantic rejected direct validation of `AlertRuleCreate` as `AlertRule`. |
| 6 | `.\.venv\Scripts\python.exe -m pytest tests -q` after using `rule_input.model_dump()` | `4 passed in 0.61s`. |

## First Run
| Step | Command | Verified result |
|---|---|---|
| 1 | `Set-Location 'd:\Databricks\options-trading-app\alerting'; .\start.ps1` | Uvicorn started on `http://127.0.0.1:8008`. |
| 2 | `POST /v1/rules`, then `POST /v1/evaluate` | Returned `alerting:ok`; a rule was created and triggered 1 alert for `NFO:NIFTY26SEP24800CE`. |

First independent run verified.

## Runbook
1. `Set-Location alerting`
2. `python -m venv .venv`
3. `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`
4. `.\start.ps1`
5. `Invoke-RestMethod http://127.0.0.1:8008/health`
6. `.\.venv\Scripts\python.exe -m pytest tests -q`

## State Model
- Rules and cooldown timestamps live only in process memory.
- Restarting the service clears them.
- Persistent user alerts require a later database-backed module.
- Automatic evaluation on streaming score events requires the future event integration; the MVP uses `POST /v1/evaluate`.

## Configuration
`SCORING_URL` is loaded from this service's `.env` and defaults to `http://127.0.0.1:8006`.
