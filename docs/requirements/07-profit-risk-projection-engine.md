# Module 7 — Profit/Risk Projection Engine

## Purpose
Estimate payoff range and risk — explicitly not a profit guarantee.

## Responsibilities
- Compute max loss (premium paid), theoretical max reward, breakeven, probability
  estimate from IV/historical distribution.

## Functional Requirements
- FR1: Compute breakeven price for CE/PE.
- FR2: Compute max risk (premium) and reward-to-risk ratio.
- FR3: Compute a probability-of-favorable-move estimate from historical
  volatility model.
- FR4: Present output as ranges/labels (e.g., "favorable," "moderate"), never
  as guaranteed profit.

## Non-Functional Requirements
- NFR1: All projections must include the model/assumptions used (auditable).

## Inputs / Outputs
- Input: contract scores (Module 6).
- Output: payoff/risk projection per contract, consumed by Alert/API modules.

## Dependencies
- Module 6.
