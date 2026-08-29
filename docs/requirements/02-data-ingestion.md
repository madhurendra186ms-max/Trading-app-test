# Module 2 — Data Ingestion

## Purpose
Pull live market data from Zerodha Kite Connect and normalize it into a common schema.

## Responsibilities
- Connect to the broker feed, parse tick data, and handle reconnects.

## Functional Requirements
- FR1: Use Zerodha Kite Connect WebSocket as the primary live market-data source.
- FR2: Normalize fields: symbol, strike, expiry, CE/PE, bid, ask, LTP, OI, volume, IV.
- FR3: Deliver normalized ticks directly to the Option Chain Engine for the MVP.
- FR4: Handle feed disconnects with automatic retry and resubscription.

## Non-Functional Requirements
- NFR1: End-to-end ingestion latency target (sub-second to low-seconds).
- NFR2: Report a reconnect event to the API; historical gap recovery requires optional persistence.

## Inputs / Outputs
- Input: Kite Connect WebSocket ticks.
- Output: normalized tick events delivered to Module 5.

## Dependencies
- Module 1 (runtime), external data provider.
