# Risk Projection API Reference

## Service
- Base URL: `http://127.0.0.1:8007`
- Protocol and format: HTTP with JSON responses
- Authentication: none for local MVP
- Interactive API: `GET /docs`
- OpenAPI schema: `GET /openapi.json`

## Endpoint Summary

| Method | Path | Request data | Success response | Purpose |
|---|---|---|---|---|
| `GET` | `/health` | None | `200 OK` | Checks service availability. |
| `GET` | `/v1/projections` | Contract query parameters | `200 OK` | Calculates long-option risk and payoff values. |

## `GET /health`

### Request
- Headers, path parameters, query parameters, and body: none

### `200 OK` Response

```json
{
  "service": "risk-projection",
  "status": "ok"
}
```

## `GET /v1/projections`

Finds a contract in the current Scoring rankings and calculates a long-option projection. It is
an estimate based on supplied values, not an order recommendation or profit guarantee.

### Request

| Parameter | Type | Required | Default | Description |
|---|---|---:|---|---|
| `index` | string | Yes | - | Underlying index, for example `NIFTY 50`. |
| `expiry` | string | Yes | - | Expiry date in `YYYY-MM-DD` format. |
| `instrument` | string | Yes | - | Exact instrument identifier from Scoring. |
| `quantity` | integer | No | `1` | Number of option units; must be greater than 0. |
| `underlying_at_expiry` | number | No | - | Scenario underlying price at expiry; must be greater than or equal to 0. |

Example:

```text
http://127.0.0.1:8007/v1/projections?index=NIFTY%2050&expiry=2026-09-04&instrument=NFO:NIFTY26SEP24800CE&quantity=1&underlying_at_expiry=25000
```

### `200 OK` Response

```json
{
  "instrument": "NFO:NIFTY26SEP24800CE",
  "option_type": "CE",
  "strike": 24800.0,
  "premium_points": 132.7,
  "quantity": 1,
  "breakeven": 24932.7,
  "max_loss_points": 132.7,
  "max_profit_points": null,
  "reward_to_risk": null,
  "scenario": {
    "underlying_at_expiry": 25000.0,
    "payoff_points": 67.3
  },
  "unavailable_factors": ["probability_of_profit"],
  "assumptions": ["Long option position."]
}
```

| Field | Description |
|---|---|
| `breakeven` | Strike plus premium for a call; strike minus premium for a put. |
| `max_loss_points` | Premium paid multiplied by quantity. |
| `max_profit_points` | `null` for a long call (unbounded); bounded for a long put. |
| `reward_to_risk` | `null` when long-call profit is unbounded; calculated for a long put. |
| `scenario.payoff_points` | Payoff at the supplied expiry underlying price, after premium. |

All returned monetary-like figures are option points, not rupees. Lot size, brokerage, taxes,
and slippage are excluded.

### Error Responses

| Status | Cause |
|---|---|
| `404 Not Found` | Instrument is absent from current Scoring rankings. |
| `422 Unprocessable Content` | Required query parameter is missing or invalid. |
| `503 Service Unavailable` | Scoring service cannot be reached. |
