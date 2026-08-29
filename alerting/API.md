# Alerting API Reference

## Service
- Base URL: `http://127.0.0.1:8008`
- Protocol and format: HTTP with JSON request/response bodies
- Authentication: none for local MVP
- Interactive API: `GET /docs`
- OpenAPI schema: `GET /openapi.json`

## Endpoint Summary

| Method | Path | Request data | Success response | Purpose |
|---|---|---|---|---|
| `GET` | `/health` | None | `200 OK` | Checks service availability. |
| `POST` | `/v1/rules` | Alert rule JSON | `201 Created` | Creates a session-only rule. |
| `GET` | `/v1/rules` | None | `200 OK` | Lists rules in this running process. |
| `POST` | `/v1/evaluate` | None | `200 OK` | Evaluates all current rules using Scoring. |

## `GET /health`

### `200 OK` Response

```json
{
  "service": "alerting",
  "status": "ok"
}
```

## `POST /v1/rules`

Creates a rule. At least one threshold is required. Rules are cleared on service restart.

### Request Body

```json
{
  "index": "NIFTY 50",
  "expiry": "2026-09-04",
  "option_type": "CE",
  "min_score": 90,
  "max_spread_percent": 1,
  "cooldown_seconds": 60
}
```

| Field | Type | Required | Default | Description |
|---|---|---:|---|---|
| `index` | string | Yes | - | Underlying index. |
| `expiry` | string | Yes | - | Expiry in `YYYY-MM-DD` format. |
| `option_type` | string | No | - | `CE` or `PE` filter. |
| `min_score` | number | Conditional | - | Trigger when score is at least this value, 0-100. |
| `max_spread_percent` | number | Conditional | - | Trigger when spread is at most this value. |
| `cooldown_seconds` | integer | No | `60` | Minimum seconds between alerts for the same rule/instrument. |

`min_score` or `max_spread_percent` must be provided.

### `201 Created` Response
Returns the submitted rule plus a generated `id`.

## `GET /v1/rules`

Returns an array of the current process's rules. An empty array means no rules exist.

## `POST /v1/evaluate`

Fetches current rankings for every rule and returns contracts that satisfy rule conditions and
are outside their cooldown interval.

### Request
- Headers, path parameters, query parameters, and body: none

### `200 OK` Response

```json
{
  "triggered": [
    {
      "rule_id": "generated-rule-id",
      "instrument": "NFO:NIFTY26SEP24800CE",
      "score": 94.37,
      "spread_percent": 0.5631,
      "triggered_at": "2026-08-29T10:30:00+00:00"
    }
  ]
}
```

## Errors

| Status | Cause |
|---|---|
| `404 Not Found` | Unknown endpoint. |
| `405 Method Not Allowed` | Unsupported HTTP method. |
| `422 Unprocessable Content` | Invalid rule data or no rule threshold. |
| `503 Service Unavailable` | Scoring service is unavailable during evaluation. |
| `500 Internal Server Error` | Unexpected service failure. |
