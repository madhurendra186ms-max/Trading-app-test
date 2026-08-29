# Module 5 and Module 6 Communication Flow

```mermaid
sequenceDiagram
    participant Scoring as Module 6: Scoring :8006
    participant Chain as Module 5: Option Chain :8005

    Scoring->>Chain: GET /v1/option-chain?index&expiry
    Chain-->>Scoring: 200 OK + paired CE/PE chain rows
    Scoring->>Scoring: calculate spread, volume, and OI components
    Scoring-->>Client: 200 OK GET /v1/rankings
```

| Direction | Method | Endpoint | Payload |
|---|---|---|---|
| Module 6 → Module 5 | `GET` | `/v1/option-chain?index={index}&expiry={expiry}` | Paired CE/PE rows by strike. |
| Client → Module 6 | `GET` | `/v1/rankings?index={index}&expiry={expiry}` | Ranked contracts with explainable score components. |

The live score uses spread (40 points), volume (30 points), and open interest (30 points).
