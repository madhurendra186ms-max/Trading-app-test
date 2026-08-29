# Market Ingestion Service Diagram

## Service Boundary

```mermaid
flowchart LR
    Source["Sample Tick Source\nCurrent MVP"]
    Kite["Zerodha Kite Connect\nFuture source"]
    Ingest["Market Ingestion\nPort 8002"]
    Chain["Option Chain Service\nPort 8005 - planned"]

    Source -->|normalized option ticks| Ingest
    Kite -. replaces sample source .-> Ingest
    Ingest -->|GET /v1/ticks| Chain
```

## Interfaces

| Endpoint | Purpose |
|---|---|
| `GET /health` | Confirms that the service is running. |
| `GET /v1/ticks` | Returns normalized sample CE/PE option ticks. |

## Local Run

```powershell
Set-Location d:\Databricks\options-trading-app\market-ingestion
.\start.ps1
```

The service is independently runnable on `http://127.0.0.1:8002`.
