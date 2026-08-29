# State Gateway Service Diagram

```mermaid
flowchart LR
    Ingestion["Market Ingestion\nPort 8002"]
    Gateway["State Gateway\nPort 8003"]
    Memory["In-Memory Tick Store"]
    Chain["Option Chain\nPort 8005 - planned"]
    Score["Scoring\nPort 8006 - planned"]

    Ingestion -. planned POST /v1/ticks .-> Gateway
    Gateway --> Memory
    Chain -->|GET /v1/ticks| Gateway
    Score -->|GET /v1/ticks| Gateway
```

The store is process-local for the MVP. Redis is an optional replacement when state must be
shared across service replicas or restored after restart. The automatic ingestion-to-gateway
post is the next integration change.
