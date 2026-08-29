# Indian Index Options Intelligence App

Real-time NIFTY/BANK NIFTY (and other top-liquidity index) option-chain monitor with
liquidity/risk-reward scoring and historical index-selection engine.

> This is a decision-support and risk-analysis tool. It does not guarantee profit and
> does not auto-execute trades.

## Stack
- Infra: OpenStack + K3s (free, self-hosted)
- Backend: FastAPI (Python), WebSockets, Kite Connect WebSocket
- Live state: in-memory option chain; Redis only when restart recovery or multiple workers is needed
- Optional persistence: PostgreSQL for users/watchlists/alerts; ClickHouse or object storage for history/backtesting
- Frontend: React + TypeScript

## Storage Approach
- The first live dashboard does not require a database.
- Add a database only when the application needs data to survive restarts, user settings,
  historical research, or backtesting.

## Structure
- `docs/architecture.md` — system architecture & data flow diagrams
- `docs/requirements/` — one requirements file per module (11 modules)

## Modules
1. Infrastructure & DevOps
2. Data Ingestion
3. Data Storage
4. Index Research & Selection Engine
5. Real-Time Option Chain Engine
6. Scoring & Ranking Engine
7. Profit/Risk Projection Engine
8. Alerting & Notification Module
9. API & Backend Services
10. Frontend / Dashboard Module
11. Backtesting & Historical Analytics Module

See `docs/requirements/` for per-module functional/non-functional requirements and
`docs/architecture.md` for the diagrams tying them together.
