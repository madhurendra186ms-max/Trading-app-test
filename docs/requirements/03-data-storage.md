# Module 3 — Data Storage

## Purpose
Provide optional persistence only for features that need data beyond the live session.

## Responsibilities
- Keep the MVP live option chain in application memory. Add Redis for shared live state
  or restart recovery, and durable storage only for saved or historical data.

## Functional Requirements
- FR1: Do not require a database for the live-only MVP.
- FR2: Optionally use Redis for latest tick and score per contract when multiple workers
  or restart recovery is required.
- FR3: Add PostgreSQL when users, watchlists, alert rules, or audit records must persist.
- FR4: Add ClickHouse or object storage when historical research/backtesting is enabled.

## Non-Functional Requirements
- NFR1: The live-only MVP must operate without durable storage.
- NFR2: Once durable storage is enabled, define retention and test backup/restore.

## Inputs / Outputs
- Input: live ticks and optional historical/user data.
- Output: optional Redis live cache and durable datasets for persistence features.

## Dependencies
- Module 1; enabled only when a persistence feature requires it.
