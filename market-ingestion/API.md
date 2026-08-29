# Market Ingestion API Reference

## Service
- Base URL: `http://127.0.0.1:8002`
- Protocol: HTTP
- Format: JSON
- Authentication: none for the local sample-data MVP
- Interactive API: `GET /docs`
- OpenAPI schema: `GET /openapi.json`

## Endpoint Summary

| Method | Path | Request data | Success response | Purpose |
|---|---|---|---|---|
| `GET` | `/health` | None | `200 OK` | Checks whether the service is available. |
| `GET` | `/v1/ticks` | None | `200 OK` | Returns the current normalized sample option ticks. |

## `GET /health`

Checks whether the service process is running and able to serve HTTP requests.

### Request
- Method: `GET`
- URL: `http://127.0.0.1:8002/health`
- Headers: no headers required
- Path parameters: none
- Query parameters: none
- Request body: none

### Success Response
- Status: `200 OK`
- Content type: `application/json`

```json
{
  "service": "market-ingestion",
  "status": "ok"
}
```

| Field | Type | Required | Description |
|---|---|---:|---|
| `service` | string | Yes | Stable service identifier: `market-ingestion`. |
| `status` | string | Yes | Health state. The current service returns `ok`. |

### PowerShell Example

```powershell
Invoke-RestMethod http://127.0.0.1:8002/health
```

### cURL Example

```bash
curl http://127.0.0.1:8002/health
```

## `GET /v1/ticks`

Returns normalized option-market ticks. The current MVP returns deterministic sample CE and PE
contracts. The endpoint shape stays the same when Kite Connect replaces the sample source.

### Request
- Method: `GET`
- URL: `http://127.0.0.1:8002/v1/ticks`
- Headers: no headers required
- Path parameters: none
- Query parameters: none
- Request body: none

### Success Response
- Status: `200 OK`
- Content type: `application/json`
- Body: JSON array of `MarketTick` objects

```json
[
  {
    "instrument": "NFO:NIFTY26SEP24800CE",
    "index": "NIFTY 50",
    "strike": 24800.0,
    "expiry": "2026-09-04",
    "option_type": "CE",
    "bid": 132.45,
    "ask": 133.2,
    "ltp": 132.7,
    "oi": 25000000,
    "volume": 2170000,
    "iv": 12.8,
    "timestamp": "2026-08-29T10:30:00+00:00"
  }
]
```

| Field | Type | Required | Rules / Description |
|---|---|---:|---|
| `instrument` | string | Yes | Provider instrument identifier. |
| `index` | string | Yes | Underlying index, for example `NIFTY 50`. |
| `strike` | number | Yes | Option strike price. |
| `expiry` | string | Yes | Expiry date in `YYYY-MM-DD` format. |
| `option_type` | string | Yes | `CE` for call option or `PE` for put option. |
| `bid` | number | Yes | Best buy price; must be greater than or equal to 0. |
| `ask` | number | Yes | Best sell price; must be greater than or equal to 0. |
| `ltp` | number | Yes | Last traded price; must be greater than or equal to 0. |
| `oi` | integer | Yes | Open interest; must be greater than or equal to 0. |
| `volume` | integer | Yes | Traded volume; must be greater than or equal to 0. |
| `iv` | number | Yes | Implied volatility percentage; must be greater than or equal to 0. |
| `timestamp` | string | Yes | UTC ISO 8601 timestamp for the tick. |

### PowerShell Example

```powershell
Invoke-RestMethod http://127.0.0.1:8002/v1/ticks
```

### cURL Example

```bash
curl http://127.0.0.1:8002/v1/ticks
```

## Error Responses

| Status | When it occurs | Response shape |
|---|---|---|
| `404 Not Found` | The method/path does not exist. | FastAPI error JSON with `detail`. |
| `405 Method Not Allowed` | A method other than `GET` is sent to these endpoints. | FastAPI error JSON with `detail`. |
| `500 Internal Server Error` | An unexpected server failure occurs. | Default server error response; do not depend on its exact shape. |

## Versioning and Compatibility
- API version prefix: `/v1` for market data endpoints.
- `/health` is intentionally unversioned for deployment checks.
- Adding a new response field is backward compatible.
- Removing or renaming a response field requires a new API version.
