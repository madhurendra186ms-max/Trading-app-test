# Module 3 — Data Storage

## Purpose
Persist raw, time-series, and relational data efficiently.

## Responsibilities
- Schema design for Postgres (metadata), ClickHouse (tick/time-series), Redis
  (hot cache), object storage (raw feed archive).

## Functional Requirements
- FR1: Postgres tables: index_master, strike_master, expiry_master, watchlist, users.
- FR2: ClickHouse tables: option_chain_snapshot, historical_option_chain, iv_surface.
- FR3: Redis: latest tick per contract, latest score per contract.
- FR4: Object storage: raw feed dumps for replay/audit.

## Non-Functional Requirements
- NFR1: Retention policy per table (e.g., raw ticks N days hot, archived cold).
- NFR2: Backup/restore procedure documented and tested.

## Inputs / Outputs
- Input: normalized ticks (Module 2/5), historical data (Module 4).
- Output: queryable datasets for Scoring, API, Backtesting modules.

## Dependencies
- Module 1.
