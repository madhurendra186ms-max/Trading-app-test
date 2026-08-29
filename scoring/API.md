# Scoring API Reference

## Service
- Base URL: `http://127.0.0.1:8006`
- Protocol and format: HTTP with JSON responses
- Authentication: none for local MVP
- Interactive API: `GET /docs`
- OpenAPI schema: `GET /openapi.json`

## Endpoint Summary

| Method | Path | Request data | Success response | Purpose |
|---|---|---|---|---|
| `GET` | `/health` | None | `200 OK` | Checks service availability. |
| `GET` | `/v1/rankings` | `index`, `expiry`, optional `option_type` | `200 OK` | Returns contracts ranked by current liquidity score. |

## `GET /health`

### Request
- Headers, path parameters, query parameters, and body: none

### `200 OK` Response

```json
{
  "service": "scoring",
  "status": "ok"
}
```

## `GET /v1/rankings`

Fetches the live option chain from Option Chain service and ranks each available CE/PE contract.

### Request

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `index` | string | Yes | Underlying index, for example `NIFTY 50`. |
| `expiry` | string | Yes | Option expiry in `YYYY-MM-DD` format. |
| `option_type` | string | No | Filter rankings to `CE` or `PE`. |

Example:

```text
http://127.0.0.1:8006/v1/rankings?index=NIFTY%2050&expiry=2026-09-04&option_type=CE
```

### `200 OK` Response

```json
{
  "index": "NIFTY 50",
  "expiry": "2026-09-04",
  "rankings": [
    {
      "instrument": "NFO:NIFTY26SEP24800CE",
      "option_type": "CE",
      "strike": 24800.0,
      "ltp": 132.7,
      "spread_percent": 0.57,
      "score": 89.4,
      "components": {
        "spread": 34.3,
        "volume": 30.0,
        "open_interest": 25.1
      }
    }
  ],
  "unavailable_factors": ["iv_rank", "momentum"]
}
```

| Field | Type | Description |
|---|---|---|
| `rankings` | array | Contracts sorted descending by live liquidity score. |
| `score` | number | Sum of spread, volume, and open-interest components; range 0-100. |
| `spread_percent` | number | $((ask - bid) / ask) * 100$. |
| `components.spread` | number | 0-40 points for lower bid-ask spread. |
| `components.volume` | number | 0-30 points for live volume. |
| `components.open_interest` | number | 0-30 points for current open interest. |
| `unavailable_factors` | array | Factors not yet calculated because historical observations are unavailable. |

### Error Responses

| Status | Cause |
|---|---|
| `422 Unprocessable Content` | Required `index`/`expiry` is absent or invalid, or `option_type` is not `CE`/`PE`. |
| `503 Service Unavailable` | Option Chain service cannot be reached. |

## Errors

| Status | Cause |
|---|---|
| `404 Not Found` | Unknown endpoint. |
| `405 Method Not Allowed` | Unsupported HTTP method. |
| `422 Unprocessable Content` | Invalid query parameter. |
| `503 Service Unavailable` | Option Chain service is unavailable. |
| `500 Internal Server Error` | Unexpected service failure. |
