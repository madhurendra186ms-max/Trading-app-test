from datetime import datetime, timezone

from chain import build_option_chain, list_expiries
from models import MarketTick, OptionType


def tick(option_type: OptionType, strike: float, expiry: str = "2026-09-04") -> MarketTick:
    suffix = "CE" if option_type is OptionType.CALL else "PE"
    return MarketTick(
        instrument=f"NFO:NIFTY26SEP{strike:.0f}{suffix}",
        index="NIFTY 50",
        strike=strike,
        expiry=expiry,
        option_type=option_type,
        bid=100,
        ask=101,
        ltp=100.5,
        oi=1000,
        volume=500,
        iv=12.5,
        timestamp=datetime.now(timezone.utc),
    )


def test_chain_pairs_call_and_put_by_strike() -> None:
    chain = build_option_chain(
        [tick(OptionType.CALL, 24800), tick(OptionType.PUT, 24800), tick(OptionType.CALL, 24900)],
        "NIFTY 50",
        "2026-09-04",
    )

    assert [row.strike for row in chain.rows] == [24800, 24900]
    assert chain.rows[0].call is not None
    assert chain.rows[0].put is not None
    assert chain.rows[1].call is not None
    assert chain.rows[1].put is None


def test_chain_excludes_other_index_and_expiry() -> None:
    other_index = tick(OptionType.PUT, 24800)
    other_index.index = "BANK NIFTY"
    chain = build_option_chain(
        [tick(OptionType.CALL, 24800), tick(OptionType.PUT, 24900, "2026-09-11"), other_index],
        "NIFTY 50",
        "2026-09-04",
    )

    assert len(chain.rows) == 1
    assert chain.rows[0].strike == 24800


def test_expiries_are_unique_and_sorted() -> None:
    expiries = list_expiries(
        [tick(OptionType.CALL, 24800, "2026-09-11"), tick(OptionType.PUT, 24800), tick(OptionType.CALL, 24900)],
        "NIFTY 50",
    )

    assert expiries == ["2026-09-04", "2026-09-11"]
