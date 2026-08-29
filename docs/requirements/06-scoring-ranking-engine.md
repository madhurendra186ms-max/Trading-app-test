# Module 6 — Scoring & Ranking Engine

## Purpose
Rank contracts by liquidity, spread, and risk-reward — not a "buy signal."

## Responsibilities
- Compute per-contract score from spread, volume, OI, IV rank, momentum.

## Functional Requirements
- FR1: Compute bid-ask spread %, OI concentration, IV rank, momentum indicator
  per contract.
- FR2: Combine into a single explainable composite score.
- FR3: Re-score on every material tick change.
- FR4: Expose "top N ranked contracts" per index/expiry.

## Non-Functional Requirements
- NFR1: Score computation must be traceable (store contributing factors, not
  just the final number).

## Inputs / Outputs
- Input: live chain state (Module 5).
- Output: contract scores written to Redis, consumed by Profit/Alert/API modules.

## Dependencies
- Module 5.
