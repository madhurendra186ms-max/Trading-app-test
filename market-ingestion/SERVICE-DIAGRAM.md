# Market Ingestion Service Diagram

## Service Boundary

```mermaid
flowchart LR
    Source["Sample Tick Source\nCurrent MVP"]
    Kite["Zerodha Kite Connect\nFuture source"]
    Ingest["Market Ingestion\nPort 8002"]
    State["State Gateway\nPort 8003"]
    Chain["Option Chain Service\nPort 8005 - planned"]

    Source -->|normalized option ticks| Ingest
    Kite -. replaces sample source .-> Ingest
    Ingest -. planned POST /v1/ticks .-> State
    State -->|GET /v1/ticks| Chain
```

## Interfaces

| Endpoint | Purpose |
|---|---|
| `GET /health` | Confirms that the service is running. |
| `GET /v1/ticks` | Returns normalized sample CE/PE option ticks. |

The next integration sends each normalized `MarketTick` to State Gateway using
`POST http://127.0.0.1:8003/v1/ticks`.

See `API.md` for request/response schemas, examples, status codes, and compatibility rules.

## Local Run

```powershell
Set-Location d:\Databricks\options-trading-app\market-ingestion
.\start.ps1
```

The service is independently runnable on `http://127.0.0.1:8002`.
