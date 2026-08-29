# Module 9 — API & Backend Services

## Purpose
Central gateway between data layer and frontend/clients.

## Responsibilities
- REST endpoints, WebSocket streaming, authentication, request routing.

## Functional Requirements
- FR1: REST: index list, watchlist CRUD, historical query, alert rule CRUD.
- FR2: WebSocket: live option chain stream, live score stream.
- FR3: AuthN/AuthZ for user accounts.

## Non-Functional Requirements
- NFR1: Rate limiting on REST endpoints.
- NFR2: Input validation on all endpoints (OWASP-aligned).

## Inputs / Outputs
- Input: data from Modules 3, 5, 6, 7, 8.
- Output: REST/WebSocket APIs consumed by frontend (Module 10).

## Dependencies
- Modules 3, 5, 6, 7, 8.
