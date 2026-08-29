# State Gateway API Reference

## Service
- Base URL: `http://127.0.0.1:8003`
- Protocol and format: HTTP with JSON request/response bodies
- Authentication: none for the local MVP
- Interactive API: `GET /docs`
- OpenAPI schema: `GET /openapi.json`

## Endpoint Summary

| Method | Path | Request data | Success response | Purpose |
|---|---|---|---|---|
| `GET` | `/health` | None | `200 OK` | Checks service availability. |
| `POST` | `/v1/ticks` | `MarketTick` JSON body | `201 Created` | Stores a tick if it is not older than existing state. |
| `GET` | `/v1/ticks` | None | `200 OK` | Lists latest ticks sorted by instrument. |
| `GET` | `/v1/ticks/{instrument}` | Instrument path parameter | `200 OK` | Returns one latest tick. |
| `GET` | `/v1/state` | None | `200 OK` | Returns live state summary. |
| `GET` | `/v1/indexes/top-volume` | None | `200 OK` | Lists up to five indexes ranked by observed option volume. |

## `GET /health`

### Request
- Headers, path parameters, query parameters, and body: none

### `200 OK` Response

```json
{
  "service": "state-gateway",
  "status": "ok"
}
```

## `POST /v1/ticks`

Stores the latest tick for `instrument`. A tick with an older `timestamp` does not overwrite
newer state; the response returns the tick currently retained.

### Request
- Content type: `application/json`
- Path parameters: none
- Query parameters: none

```json
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
```

| Field | Type | Required | Rules |
|---|---|---:|---|
| `instrument` | string | Yes | Non-empty provider instrument identifier. |
| `index` | string | Yes | Non-empty underlying index name. |
| `strike` | number | Yes | Greater than or equal to 0. |
| `expiry` | string | Yes | Non-empty expiry date, convention `YYYY-MM-DD`. |
| `option_type` | string | Yes | `CE` or `PE`. |
| `bid`, `ask`, `ltp`, `iv` | number | Yes | Each must be greater than or equal to 0. |
| `oi`, `volume` | integer | Yes | Each must be greater than or equal to 0. |
| `timestamp` | string | No | ISO 8601 timestamp; defaults to the current UTC time. |

### `201 Created` Response
Returns the current `MarketTick` for the instrument using the same schema as the request.

### PowerShell Example

```powershell
$tick = @{ instrument = 'NFO:NIFTY26SEP24800CE'; index = 'NIFTY 50'; strike = 24800; expiry = '2026-09-04'; option_type = 'CE'; bid = 132.45; ask = 133.20; ltp = 132.70; oi = 25000000; volume = 2170000; iv = 12.8 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8003/v1/ticks -ContentType 'application/json' -Body $tick
```

## `GET /v1/ticks`

### Request
- Headers, path parameters, query parameters, and body: none

### `200 OK` Response
Returns an array of `MarketTick` objects, sorted by `instrument`. Returns `[]` when no data has
been stored in the current service process.

## `GET /v1/ticks/{instrument}`

### Request
- Path parameter: `instrument` (string, required)
- Headers, query parameters, and body: none

### `200 OK` Response
Returns one `MarketTick` object.

### `404 Not Found` Response

```json
{
  "detail": "Instrument was not found"
}
```

## `GET /v1/state`

### Request
- Headers, path parameters, query parameters, and body: none

### `200 OK` Response

```json
{
  "instruments": 1
}
```

| Field | Type | Description |
|---|---|---|
| `instruments` | integer | Count of instruments stored in the running process. |

## `GET /v1/indexes/top-volume`

### Request
- Headers, path parameters, query parameters, and body: none

### `200 OK` Response

```json
[
  {
    "index": "NIFTY 50",
    "option_volume": 4220000
  }
]
```

`option_volume` is the sum of current CE and PE tick volumes for each index. The endpoint returns
at most five indexes and only includes indexes currently ingested into this running service.

## Errors

| Status | Cause |
|---|---|
| `404 Not Found` | Unknown endpoint or unknown instrument. |
| `405 Method Not Allowed` | Unsupported HTTP method. |
| `422 Unprocessable Content` | Invalid or missing `MarketTick` request fields. |
| `500 Internal Server Error` | Unexpected server failure. |
