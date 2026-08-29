from engine import project_long_option
from models import ContractScore, OptionType


def contract(option_type: OptionType) -> ContractScore:
    suffix = "CE" if option_type is OptionType.CALL else "PE"
    return ContractScore(
        instrument=f"NFO:NIFTY26SEP24800{suffix}",
        option_type=option_type,
        strike=24800,
        ltp=100,
        score=90,
    )


def test_long_call_has_breakeven_and_unlimited_profit() -> None:
    projection = project_long_option(contract(OptionType.CALL), quantity=2, underlying_at_expiry=25050)

    assert projection.breakeven == 24900
    assert projection.max_loss_points == 200
    assert projection.max_profit_points is None
    assert projection.reward_to_risk is None
    assert projection.scenario is not None
    assert projection.scenario.payoff_points == 300


def test_long_put_has_bounded_profit_and_payoff() -> None:
    projection = project_long_option(contract(OptionType.PUT), quantity=2, underlying_at_expiry=24500)

    assert projection.breakeven == 24700
    assert projection.max_loss_points == 200
    assert projection.max_profit_points == 49400
    assert projection.reward_to_risk == 247
    assert projection.scenario is not None
    assert projection.scenario.payoff_points == 400


def test_projection_without_scenario_has_no_payoff_value() -> None:
    projection = project_long_option(contract(OptionType.CALL), quantity=1)

    assert projection.scenario is None
    assert projection.unavailable_factors == ["probability_of_profit"]
