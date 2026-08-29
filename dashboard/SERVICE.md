# Dashboard Service

## Purpose
Provides the trader-facing Market Desk. It calls only API Gateway and never connects directly to market-data or broker services.

## Interface
- Port: `8010`
- Browser URL: `http://127.0.0.1:8010`
- Upstream: API Gateway (`8009`)
- API gateway request: `GET /v1/dashboard?index=NIFTY%2050&expiry=2026-09-04`
- Service diagram: `SERVICE-DIAGRAM.md`

## Setup Log
| Step | Command | Verified result |
|---|---|---|
| 1 | `node --version; npm --version`; port check for `8010` | Node `v22.22.0`, npm `11.17.0`; port `8010` was available. |
| 2 | `npx create-vite@latest dashboard --template react-ts --no-interactive` | Created Vite React/TypeScript dashboard scaffold. |
| 3 | `npm install; npm install lucide-react` | Installed 29 packages; audit reported 0 vulnerabilities. |
| 4 | `npm run build` | TypeScript and Vite production build completed successfully. |
| 5 | `npm run build` after top-volume index selector | Production build completed successfully. |

## First Run
| Step | Command | Verified result |
|---|---|---|
| 1 | `npm run build` | Production build passed; 1,818 modules transformed. |
| 2 | `npm run dev -- --port 8010` | Vite started at `http://localhost:8010/`. |
| 3 | `Invoke-WebRequest http://localhost:8010` | Returned `200 OK`. |
| 4 | `GET :8009/v1/dashboard` | Gateway returned 1 chain row and 2 rankings. |
| 5 | Browser-origin request to API Gateway using `Origin: http://localhost:8010` | Returned `200` with matching `Access-Control-Allow-Origin`. |

First independent run verified.

## Runbook
1. `Set-Location dashboard`
2. `npm install`
3. `npm run dev -- --port 8010`
4. Open `http://127.0.0.1:8010`
5. `npm run build`

## Configuration
`VITE_API_GATEWAY_URL` is loaded from `.env` and defaults to `http://127.0.0.1:8009`.

## Limitations
- The desk updates when the user presses refresh; WebSocket streaming is a later addition.
- The Prepare Trade button is intentionally non-executing.
- Sample data appears if API Gateway is unavailable.
- The selector ranks only indexes currently present in State Gateway. It currently has one choice because Market Ingestion supplies NIFTY 50 samples only.
