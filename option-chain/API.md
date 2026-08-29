# Option Chain API Reference

## Service
- Base URL: `http://127.0.0.1:8005`
- Protocol and format: HTTP with JSON responses
- Authentication: none for local MVP
- Interactive API: `GET /docs`
- OpenAPI schema: `GET /openapi.json`

## Endpoint Summary

| Method | Path | Request data | Success response | Purpose |
|---|---|---|---|---|
| `GET` | `/health` | None | `200 OK` | Checks service availability. |
| `GET` | `/v1/option-chain` | `index`, `expiry` query parameters | `200 OK` | Returns CE/PE rows grouped by strike. |
| `GET` | `/v1/option-chain/expiries` | `index` query parameter | `200 OK` | Lists current expiries for an index. |

## `GET /health`

### Request
- Headers, path parameters, query parameters, and body: none

### `200 OK` Response

```json
{
  "service": "option-chain",
  "status": "ok"
}
```

## `GET /v1/option-chain`

Fetches current ticks from State Gateway and pairs call and put ticks at every matching strike.

### Request
- Method: `GET`
- Query parameters:

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `index` | string | Yes | Underlying index, for example `NIFTY 50`. |
| `expiry` | string | Yes | Option expiry in `YYYY-MM-DD` format. |

Example:

```text
http://127.0.0.1:8005/v1/option-chain?index=NIFTY%2050&expiry=2026-09-04
```

### `200 OK` Response

```json
{
  "index": "NIFTY 50",
  "expiry": "2026-09-04",
  "rows": [
    {
      "strike": 24800.0,
      "call": { "instrument": "NFO:NIFTY26SEP24800CE", "option_type": "CE" },
      "put": { "instrument": "NFO:NIFTY26SEP24800PE", "option_type": "PE" }
    }
  ]
}
```

Each non-null `call` or `put` has the complete `MarketTick` schema: `instrument`, `index`,
`strike`, `expiry`, `option_type`, `bid`, `ask`, `ltp`, `oi`, `volume`, `iv`, and `timestamp`.

### Error Responses

| Status | Cause |
|---|---|
| `422 Unprocessable Content` | `index` or `expiry` is missing or empty. |
| `503 Service Unavailable` | State Gateway cannot be reached or returned an error. |

## `GET /v1/option-chain/expiries`

### Request
- Method: `GET`
- Query parameter: `index` (string, required)

Example:

```text
http://127.0.0.1:8005/v1/option-chain/expiries?index=NIFTY%2050
```

### `200 OK` Response

```json
{
  "index": "NIFTY 50",
  "expiries": ["2026-09-04"]
}
```

## Errors

| Status | Cause |
|---|---|
| `404 Not Found` | Unknown endpoint. |
| `405 Method Not Allowed` | Unsupported HTTP method. |
| `422 Unprocessable Content` | Invalid or missing query parameter. |
| `503 Service Unavailable` | State Gateway is unavailable. |
| `500 Internal Server Error` | Unexpected service failure. |
