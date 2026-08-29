# Module 6, Module 7, and Module 8 Communication Flow

```mermaid
flowchart LR
    Score["Module 6: Scoring\n:8006"]
    Risk["Module 7: Risk Projection\n:8007"]
    Alert["Module 8: Alerting\n:8008"]
    Client["Client / API Gateway"]

    Risk -->|GET /v1/rankings| Score
    Alert -->|GET /v1/rankings| Score
    Client -->|GET /v1/projections| Risk
    Client -->|POST /v1/evaluate| Alert
```

| Consumer | Upstream call | Result |
|---|---|---|
| Module 7 | `GET :8006/v1/rankings?index&expiry` | Finds the selected contract and computes payoff/risk in option points. |
| Module 8 | `GET :8006/v1/rankings?index&expiry` | Evaluates session-only score/spread alert rules. |

Module 7 does not claim profit or return rupee values. Module 8 applies per-rule/per-instrument cooldowns.
