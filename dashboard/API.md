# Dashboard API Integration

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `VITE_API_GATEWAY_URL` | `http://127.0.0.1:8009` | Base URL for the Dashboard's only backend dependency. |

## Gateway Requests

| Method | Gateway path | Request | Used for |
|---|---|---|---|
| `GET` | `/v1/dashboard` | `index`, `expiry` query parameters | Option chain rows, rankings, and alert count. |
| `GET` | `/v1/projections` | Selected contract parameters | Future detailed trade-review panel. |
| `GET` | `/v1/indexes/top-volume` | None | Up to five indexes ranked by current observed option volume. |

The index selector calls `/v1/indexes/top-volume` once on page load. It displays only indexes
currently ingested into State Gateway, with a maximum of five. The app renders a clearly-labeled
sample fallback when API Gateway is unavailable. It never sends credentials or order requests.
