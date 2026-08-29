# Module 3 and Module 5 Communication Flow

```mermaid
sequenceDiagram
    participant State as Module 3: State Gateway :8003
    participant Chain as Module 5: Option Chain :8005

    Chain->>State: GET /v1/ticks
    State-->>Chain: 200 OK + current MarketTick array
    Chain->>Chain: group by index, expiry, strike; pair CE and PE
    Chain-->>Client: 200 OK GET /v1/option-chain
```

| Direction | Method | Endpoint | Payload |
|---|---|---|---|
| Module 5 → Module 3 | `GET` | `/v1/ticks` | No request body; returns current normalized ticks. |
| Client → Module 5 | `GET` | `/v1/option-chain?index={index}&expiry={expiry}` | Returns strike rows containing `call` and `put` tick objects. |

Module 5 never stores ticks. It rebuilds an option-chain response from the current Module 3 state.
