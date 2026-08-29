from models import ContractScore, OptionType, PayoffScenario, RiskProjection


def project_long_option(
    contract: ContractScore, quantity: int, underlying_at_expiry: float | None = None
) -> RiskProjection:
    premium = contract.ltp
    max_loss = premium * quantity
    if contract.option_type is OptionType.CALL:
        breakeven = contract.strike + premium
        max_profit = None
        reward_to_risk = None
    else:
        breakeven = max(0.0, contract.strike - premium)
        max_profit = max(0.0, contract.strike - premium) * quantity
        reward_to_risk = round(max_profit / max_loss, 4) if max_loss else None

    scenario = None
    if underlying_at_expiry is not None:
        intrinsic = max(0.0, underlying_at_expiry - contract.strike)
        if contract.option_type is OptionType.PUT:
            intrinsic = max(0.0, contract.strike - underlying_at_expiry)
        scenario = PayoffScenario(
            underlying_at_expiry=underlying_at_expiry,
            payoff_points=round((intrinsic - premium) * quantity, 2),
        )

    return RiskProjection(
        instrument=contract.instrument,
        option_type=contract.option_type,
        strike=contract.strike,
        premium_points=premium,
        quantity=quantity,
        breakeven=round(breakeven, 2),
        max_loss_points=round(max_loss, 2),
        max_profit_points=round(max_profit, 2) if max_profit is not None else None,
        reward_to_risk=reward_to_risk,
        scenario=scenario,
        unavailable_factors=["probability_of_profit"],
        assumptions=[
            "Long option position.",
            "Premium and payoff are option points, not rupees.",
            "Broker lot size, taxes, charges, and slippage are excluded.",
        ],
    )
