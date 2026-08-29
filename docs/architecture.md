# System Architecture & Data Flow

## Module relationship diagram

```mermaid
graph TB
    subgraph Infra["1. Infrastructure & DevOps"]
        OS[OpenStack] --> K3S[K3s Cluster]
    end

    subgraph Ingest["2. Data Ingestion"]
        FEED[Zerodha Kite Connect WebSocket] --> NORM[Normalizer]
    end

    subgraph Live["Live State: required for MVP"]
        MEM[In-Memory Option Chain]
        REDIS[(Optional Redis)]
    end

    subgraph Research["4. Index Selection Engine"]
        HIST[20yr Historical Data] --> RANK[Liquidity Ranking Model]
        RANK --> TOP5[Top 5 Index List]
    end

    subgraph Chain["5. Real-Time Option Chain Engine"]
        NORM --> OCE[Option Chain Processor]
        OCE --> MEM
        OCE -. optional .-> REDIS
    end

    subgraph Score["6. Scoring & Ranking Engine"]
        OCE --> SCORE[Contract Scorer]
        SCORE --> MEM
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
    MEM --> API
    SCORE --> WS
    OCE --> WS

    subgraph FE["10. Frontend Dashboard"]
        UI[React App]
    end
    API --> UI
    WS --> UI

    subgraph Persist["Optional persistence: add when needed"]
        PG[(PostgreSQL)]
        CH[(ClickHouse)]
        OBJ[(Object Storage)]
    end

    subgraph Backtest["11. Backtesting Module"]
        CH --> BT[Strategy Backtester]
    end

    TOP5 --> PG
```

## End-to-end data flow (live tick to user alert)

```mermaid
sequenceDiagram
    participant Feed as Broker/NSE Feed
    participant Ingest as Ingestion Service
    participant Chain as Option Chain Engine
    participant Score as Scoring Engine
    participant State as In-Memory State
    participant API as FastAPI + WebSocket
    participant UI as React Dashboard
    participant Alert as Alert Engine

    Feed->>Ingest: raw tick (bid/ask/OI/IV)
    Ingest->>Chain: normalized event
    Chain->>State: update live option chain state
    Chain->>Score: trigger re-score
    Score->>State: write contract score + risk-reward
    State->>API: read on request / push update
    API->>UI: WebSocket push (live table update)
    Score->>Alert: evaluate threshold rules
    Alert->>UI: push notification if matched
```

## Notes
- The MVP live path uses Kite Connect, FastAPI, and in-memory state. Redis is optional;
    PostgreSQL, ClickHouse, and object storage are added only for durable data or historical analysis.
- Modules 4 (Index Selection) and 11 (Backtesting) are analytics-only and decoupled
  from the live tick path so they can be developed/tested independently.
- Scoring and Profit/Risk modules are explicitly decision-support outputs, not trade
  signals or profit guarantees.
