# Module 9 — API & Backend Services

## Purpose
Central gateway between data layer and frontend/clients.

## Responsibilities
- REST endpoints, WebSocket streaming, authentication, request routing.

## Functional Requirements
- FR1: MVP REST: live index list and current option-chain/score queries.
- FR2: WebSocket: live option chain stream, live score stream.
- FR3: Add watchlist CRUD, historical queries, alert rule CRUD, and AuthN/AuthZ
	only when user data must persist.

## Non-Functional Requirements
- NFR1: Rate limiting on REST endpoints.
- NFR2: Input validation on all endpoints (OWASP-aligned).

## Inputs / Outputs
- Input: live in-memory state from Modules 5, 6, 7, and 8; optional Module 3 data.
- Output: REST/WebSocket APIs consumed by frontend (Module 10).

## Dependencies
- Modules 5, 6, 7, 8; Module 3 only for persistent or historical endpoints.
