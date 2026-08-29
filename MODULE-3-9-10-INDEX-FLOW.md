# Modules 3, 9, and 10 Index Selection Flow

```mermaid
sequenceDiagram
    participant State as Module 3: State Gateway :8003
    participant Gateway as Module 9: API Gateway :8009
    participant Dashboard as Module 10: Dashboard :8010
    participant Trader as Trader

    Trader->>Dashboard: Open Market Desk
    Dashboard->>Gateway: GET /v1/indexes/top-volume
    Gateway->>State: GET /v1/indexes/top-volume
    State->>State: Sum current option volume by index
    State-->>Gateway: Up to 5 ranked indexes
    Gateway-->>Dashboard: Up to 5 ranked indexes
    Dashboard-->>Trader: Show index selector
    Trader->>Dashboard: Select an index
    Dashboard->>Gateway: GET /v1/dashboard?index&expiry
    Gateway-->>Dashboard: Option chain, rankings, and alerts
```

| Service | Endpoint | Responsibility |
|---|---|---|
| State Gateway | `GET /v1/indexes/top-volume` | Aggregates current CE/PE tick volume per index and returns at most five. |
| API Gateway | `GET /v1/indexes/top-volume` | Proxies the State Gateway ranking to the browser-facing API. |
| Dashboard | Gateway request on page load | Renders the selector and reloads desk data after index selection. |

This is an intraday observed-volume ranking. It shows only indexes currently ingested by Module 2
and retained in Module 3. It is not the separate 20-year historical liquidity ranking.
