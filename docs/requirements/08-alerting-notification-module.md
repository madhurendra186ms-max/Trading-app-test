# Module 8 — Alerting & Notification Module

## Purpose
Notify users when contracts match saved criteria.

## Responsibilities
- Evaluate user-defined rules against live scores/projections, dispatch
  notifications.

## Functional Requirements
- FR1: Support session-only alert rules for the MVP (e.g., spread < X, score > Y,
  index = Z).
- FR2: Rule evaluation on each score update.
- FR3: Delivery via WebSocket push, email, or webhook.
- FR4: Persist alert rules only when users need them after logout or restart.

## Non-Functional Requirements
- NFR1: No duplicate alert spam (dedup/cooldown window).

## Inputs / Outputs
- Input: contract scores (Module 6), projections (Module 7), user rules (Module 9).
- Output: notifications delivered to user via API/WebSocket/email/webhook.

## Dependencies
- Module 6, Module 7, Module 9; Module 3 only for persistent rules/history.
