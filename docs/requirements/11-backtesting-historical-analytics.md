# Module 11 — Backtesting & Historical Analytics

## Purpose
Validate scoring/ranking logic against historical data before trusting it live.

## Responsibilities
- Replay historical option chain data through scoring engine, measure
  hypothetical outcomes.

## Functional Requirements
- FR1: Replay historical option chain data through Module 6/7 logic.
- FR2: Report hit-rate, average payoff, drawdown for a given rule set.
- FR3: Support parameter tuning (backtest with different score weights).

## Non-Functional Requirements
- NFR1: Backtest results must be clearly labeled as historical/hypothetical,
  not predictive guarantees.

## Inputs / Outputs
- Input: historical data (Module 3), scoring/profit logic (Module 6, 7).
- Output: backtest reports for tuning scoring parameters.

## Dependencies
- Module 3, Module 6, Module 7.
