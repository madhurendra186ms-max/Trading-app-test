# Market Ingestion API Reference

## Service
- Base URL: `http://127.0.0.1:8002`
- Protocol: HTTP
- Format: JSON
- Authentication: none for the local sample-data MVP
- Interactive API: `GET /docs`
- OpenAPI schema: `GET /openapi.json`

## Local Configuration

The application loads `.env` from this service folder on startup. Configuration is used by the
future Kite Connect adapter and is not exposed by an API response or application logs.

| Variable | Required now | Required for Kite Connect | Purpose |
|---|---:|---:|---|
| `KITE_API_KEY` | No | Yes | Identifies your Kite Connect application. |
| `KITE_API_SECRET` | No | Yes | Used only by the backend to create a Kite session. |
| `KITE_ACCESS_TOKEN` | No | Yes | Authenticates the Kite REST/WebSocket session. |
| `KITE_REDIRECT_URL` | No | Yes | Must match the redirect URL configured in Kite Connect. |

The local `.env` file is excluded from Git. Never place its secret values in requests, API
documentation, chat, or source code.

## Endpoint Summary

| Method | Path | Request data | Success response | Purpose |
|---|---|---|---|---|
| `GET` | `/health` | None | `200 OK` | Checks whether the service is available. |
| `GET` | `/v1/auth/kite/login` | None | `307 Temporary Redirect` | Starts the Kite Connect authorization flow. |
| `GET` | `/v1/auth/kite/callback` | Kite query parameters | `200 OK` | Exchanges a one-time Kite request token for an in-memory session. |
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

## `GET /v1/auth/kite/login`

Starts the Zerodha Kite Connect login flow. It does not accept or return the API secret,
access token, password, or TOTP. The browser is redirected to Zerodha.

### Request
- Method: `GET`
- URL: `http://127.0.0.1:8002/v1/auth/kite/login`
- Headers: no headers required
- Path parameters: none
- Query parameters: none
- Request body: none
- Required local configuration: `KITE_API_KEY`

### Success Response
- Status: `307 Temporary Redirect`
- Response body: empty
- `Location` header: Kite authorization URL

Open this address in a browser:

```text
http://127.0.0.1:8002/v1/auth/kite/login
```

After approval, Kite redirects the browser to the `KITE_REDIRECT_URL` configured in your
Kite developer application, where the callback endpoint completes the daily access-token exchange.

### Error Response

```json
{
  "detail": "KITE_API_KEY is not configured"
}
```

- Status: `503 Service Unavailable`
- Cause: `KITE_API_KEY` is missing or empty in `.env`.

## `GET /v1/auth/kite/callback`

Receives the browser redirect after Kite login and exchanges Kite's one-time `request_token`
server-side. The resulting access token is retained only in this running process and is never
included in the response, logs, or `.env` file.

### Request
- Method: `GET`
- URL: `http://127.0.0.1:8002/v1/auth/kite/callback`
- Headers: no headers required
- Request body: none
- Query parameters:

| Parameter | Type | Required | Source | Description |
|---|---|---:|---|---|
| `request_token` | string | Yes | Kite redirect | Short-lived token used once to establish the session. |
| `status` | string | No | Kite redirect | Must be `success`; defaults to `success` for local API testing. |
| `type` | string | No | Kite redirect | Informational Kite login type; ignored by this service. |
| `action` | string | No | Kite redirect | Informational Kite action; ignored by this service. |

Do not manually copy a `request_token` into chat, source code, or documentation. Open the
login endpoint in a browser and let Kite redirect the browser to this callback automatically.

### Success Response
- Status: `200 OK`
- Content type: `application/json`

```json
{
  "authenticated": true,
  "message": "Kite session established"
}
```

| Field | Type | Description |
|---|---|---|
| `authenticated` | boolean | `true` only after a Kite access token was created and retained in memory. |
| `message` | string | Non-sensitive result message. |

### Error Responses

| Status | Cause | Response shape |
|---|---|---|
| `400 Bad Request` | Kite reports a status other than `success`. | FastAPI error JSON with `detail`. |
| `422 Unprocessable Content` | `request_token` is absent. | FastAPI validation error JSON. |
| `502 Bad Gateway` | Kite rejects or cannot exchange the request token. | FastAPI error JSON with a non-sensitive `detail`. |
| `503 Service Unavailable` | `KITE_API_KEY` or `KITE_API_SECRET` is missing. | FastAPI error JSON with `detail`. |

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
| `503 Service Unavailable` | Required Kite configuration is missing. | FastAPI error JSON with `detail`; no secret values are returned. |
| `500 Internal Server Error` | An unexpected server failure occurs. | Default server error response; do not depend on its exact shape. |

## Versioning and Compatibility
- API version prefix: `/v1` for market data endpoints.
- `/health` is intentionally unversioned for deployment checks.
- Adding a new response field is backward compatible.
- Removing or renaming a response field requires a new API version.
