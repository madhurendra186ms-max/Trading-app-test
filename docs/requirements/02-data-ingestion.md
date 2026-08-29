# Module 2 — Data Ingestion

## Purpose
Pull live and historical market data and normalize it into a common schema.

## Responsibilities
- Connect to broker/exchange feed, parse tick data, publish to Kafka topics, handle
  reconnect/backfill.

## Functional Requirements
- FR1: Support at least one live option-chain data source (broker API/vendor feed).
- FR2: Normalize fields: symbol, strike, expiry, CE/PE, bid, ask, LTP, OI, volume, IV.
- FR3: Publish per-index Kafka topics.
- FR4: Handle feed disconnects with automatic retry and gap-fill.

## Non-Functional Requirements
- NFR1: End-to-end ingestion latency target (sub-second to low-seconds).
- NFR2: No data loss on broker reconnect.

## Inputs / Outputs
- Input: raw broker/exchange feed (WebSocket/REST).
- Output: normalized tick events on Kafka/Redpanda topics.

## Dependencies
- Module 1 (runtime), external data provider.
