# Module 5 — Real-Time Option Chain Engine

## Purpose
Maintain live, consistent in-memory option chain state per index/expiry/strike.

## Responsibilities
- Receive normalized Kite Connect ticks, merge them into current in-memory chain state,
  and optionally mirror that state to Redis.

## Functional Requirements
- FR1: Maintain live chain for each selected index and expiry.
- FR2: Update on every tick with minimal duplicate writes.
- FR3: Expose the in-memory chain snapshot to Scoring and API modules.
- FR4: Mirror state to Redis only when shared state or restart recovery is needed.

## Non-Functional Requirements
- NFR1: Consistent state under out-of-order ticks.
- NFR2: Support a single-process in-memory MVP; add Redis before scaling across workers.

## Inputs / Outputs
- Input: normalized ticks from Module 2.
- Output: live in-memory chain state; optional Redis mirror.

## Dependencies
- Module 2; Module 3 only when optional persistence is enabled.
