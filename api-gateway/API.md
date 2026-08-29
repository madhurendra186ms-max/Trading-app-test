# API Gateway Reference

## Service
- Base URL: `http://127.0.0.1:8009`
- Protocol and format: HTTP with JSON responses
- Authentication: none for local MVP
- Allowed browser origins: `http://127.0.0.1:8010` and `http://localhost:8010` by default
- Interactive API: `GET /docs`
- OpenAPI schema: `GET /openapi.json`

## Endpoint Summary

| Method | Path | Request data | Success response | Purpose |
|---|---|---|---|---|
| `GET` | `/health` | None | `200 OK` | Checks gateway availability. |
| `GET` | `/v1/indexes/top-volume` | None | `200 OK` | Proxies up to five observed indexes ranked by option volume. |
| `GET` | `/v1/dashboard` | `index`, `expiry` query parameters | `200 OK` | Aggregates chain, rankings, and active rule count. |
| `GET` | `/v1/projections` | Projection query parameters | `200 OK` | Proxies a selected-contract projection. |

## `GET /health`

### `200 OK` Response

```json
{
  "service": "api-gateway",
  "status": "ok"
}
```

## `GET /v1/indexes/top-volume`

Returns up to five indexes ranked by current option volume from State Gateway. It is the source
for the Dashboard index selector, not a historical 20-year liquidity ranking.

### `200 OK` Response

```json
[
  { "index": "NIFTY 50", "option_volume": 4220000 }
]
```

## `GET /v1/dashboard`

### Request

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `index` | string | Yes | Underlying index, for example `NIFTY 50`. |
| `expiry` | string | Yes | Expiry date in `YYYY-MM-DD` format. |

Example:

```text
http://127.0.0.1:8009/v1/dashboard?index=NIFTY%2050&expiry=2026-09-04
```

### `200 OK` Response

```json
{
  "index": "NIFTY 50",
  "expiry": "2026-09-04",
  "option_chain": { "rows": [] },
  "rankings": { "rankings": [] },
  "active_alert_rules": 1
}
```

`option_chain` and `rankings` preserve their respective upstream API response shapes.

## `GET /v1/projections`

Forwards the following query parameters to Risk Projection: `index`, `expiry`, `instrument`, optional
`quantity` (default `1`), and optional `underlying_at_expiry`.

Example:

```text
http://127.0.0.1:8009/v1/projections?index=NIFTY%2050&expiry=2026-09-04&instrument=NFO:NIFTY26SEP24800CE&quantity=1
```

The response preserves Risk Projection's response shape and units: option points, not rupees.

## Errors

| Status | Cause |
|---|---|
| `404 Not Found` | Unknown endpoint, or propagated selected-contract absence from Risk Projection. |
| `422 Unprocessable Content` | Missing or invalid query parameter. |
| `503 Service Unavailable` | An upstream live-data service cannot be reached. |
| `500 Internal Server Error` | Unexpected gateway failure. |
