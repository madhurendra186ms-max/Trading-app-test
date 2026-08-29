# System Architecture & Data Flow

## Module relationship diagram

```mermaid
graph TB
    subgraph Infra["1. Infrastructure & DevOps"]
        OS[OpenStack] --> K3S[K3s Cluster]
    end

    subgraph Ingest["2. Data Ingestion"]
        FEED[Market Data Feed / Broker API] --> NORM[Normalizer]
        NORM --> KAFKA[Kafka/Redpanda Topics]
    end

    subgraph Store["3. Data Storage"]
        PG[(PostgreSQL)]
        CH[(ClickHouse)]
        REDIS[(Redis)]
        OBJ[(MinIO/Ceph)]
    end

    subgraph Research["4. Index Selection Engine"]
        HIST[20yr Historical Data] --> RANK[Liquidity Ranking Model]
        RANK --> TOP5[Top 5 Index List]
    end

    subgraph Chain["5. Real-Time Option Chain Engine"]
        KAFKA --> OCE[Option Chain Processor]
        OCE --> REDIS
        OCE --> CH
    end

    subgraph Score["6. Scoring & Ranking Engine"]
        OCE --> SCORE[Contract Scorer]
        SCORE --> REDIS
    end

    subgraph Profit["7. Profit/Risk Projection Engine"]
        SCORE --> PROJ[Payoff Estimator]
    end

    subgraph Alert["8. Alerting Module"]
        SCORE --> ALERTRULE[Rule Evaluator]
        PROJ --> ALERTRULE
        ALERTRULE --> NOTIFY[Push/Email/Webhook]
    end

    subgraph Backend["9. API & Backend Services"]
        API[FastAPI Gateway]
        WS[WebSocket Server]
    end
    REDIS --> API
    CH --> API
    PG --> API
    SCORE --> WS
    OCE --> WS

    subgraph FE["10. Frontend Dashboard"]
        UI[React App]
    end
    API --> UI
    WS --> UI

    subgraph Backtest["11. Backtesting Module"]
        CH --> BT[Strategy Backtester]
        BT --> PG
    end

    TOP5 --> PG
```

## End-to-end data flow (live tick to user alert)

```mermaid
sequenceDiagram
    participant Feed as Broker/NSE Feed
    participant Ingest as Ingestion Service
    participant Kafka as Kafka/Redpanda
    participant Chain as Option Chain Engine
    participant Score as Scoring Engine
    participant Redis as Redis Cache
    participant API as FastAPI + WebSocket
    participant UI as React Dashboard
    participant Alert as Alert Engine

    Feed->>Ingest: raw tick (bid/ask/OI/IV)
    Ingest->>Kafka: normalized event
    Kafka->>Chain: consume tick
    Chain->>Redis: update live option chain state
    Chain->>Score: trigger re-score
    Score->>Redis: write contract score + risk-reward
    Redis->>API: read on request / push update
    API->>UI: WebSocket push (live table update)
    Score->>Alert: evaluate threshold rules
    Alert->>UI: push notification if matched
```

## Notes
- Modules 4 (Index Selection) and 11 (Backtesting) are analytics-only and decoupled
  from the live tick path so they can be developed/tested independently.
- Scoring and Profit/Risk modules are explicitly decision-support outputs, not trade
  signals or profit guarantees.
