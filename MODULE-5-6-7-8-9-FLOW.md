# Modules 5, 6, 7, 8, and 9 Communication Flow

```mermaid
sequenceDiagram
    participant UI as React Dashboard :8010 planned
    participant Gateway as Module 9: API Gateway :8009
    participant Chain as Module 5: Option Chain :8005
    participant Score as Module 6: Scoring :8006
    participant Risk as Module 7: Risk Projection :8007
    participant Alert as Module 8: Alerting :8008

    UI->>Gateway: GET /v1/dashboard?index&expiry
    par Aggregate option chain
        Gateway->>Chain: GET /v1/option-chain
        Chain-->>Gateway: paired CE/PE rows
    and Aggregate rankings
        Gateway->>Score: GET /v1/rankings
        Score-->>Gateway: ranked contracts
    and Count rules
        Gateway->>Alert: GET /v1/rules
        Alert-->>Gateway: session rule list
    end
    Gateway-->>UI: dashboard JSON

    UI->>Gateway: GET /v1/projections?instrument&...
    Gateway->>Risk: GET /v1/projections?instrument&...
    Risk-->>Gateway: risk projection JSON
    Gateway-->>UI: risk projection JSON
```

Module 9 aggregates data at request time and does not persist it. The Dashboard service is the
next module and will only call API Gateway, never the internal services directly.
