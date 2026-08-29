# Module 5 — Real-Time Option Chain Engine

## Purpose
Maintain live, consistent in-memory option chain state per index/expiry/strike.

## Responsibilities
- Consume Kafka ticks, merge into current chain state, write to Redis/ClickHouse.

## Functional Requirements
- FR1: Maintain live chain for each selected index and expiry.
- FR2: Update on every tick with minimal duplicate writes.
- FR3: Expose current chain snapshot to Scoring and API modules.

## Non-Functional Requirements
- NFR1: Consistent state under out-of-order ticks.
- NFR2: Horizontal scalability per index/topic.

## Inputs / Outputs
- Input: normalized ticks from Kafka/Redpanda (Module 2).
- Output: live chain state in Redis, snapshots in ClickHouse.

## Dependencies
- Module 2, Module 3.
