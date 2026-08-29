# Module 4 — Index Research & Selection Engine

## Purpose
Analyze 20 years of historical data to rank and select top 3-5 liquid indexes.

## Responsibilities
- Compute historical turnover, OI depth, spread quality, strike/expiry activity;
  rank indexes.

## Functional Requirements
- FR1: Ingest 20-year historical OHLC + options turnover per index.
- FR2: Compute liquidity score per index (weighted: volume, OI depth, spread
  stability, expiry count).
- FR3: Output ranked top-5 list, refreshable periodically (e.g., quarterly).

## Non-Functional Requirements
- NFR1: Ranking must be reproducible and explainable (store weights/criteria used).

## Inputs / Outputs
- Input: 20-year historical index/options data.
- Output: ranked top-5 index list stored in Postgres.

## Dependencies
- Module 3 (historical data store).
