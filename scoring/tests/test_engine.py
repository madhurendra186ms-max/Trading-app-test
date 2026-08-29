from datetime import datetime, timezone

from engine import rank_option_chain, score_tick, spread_percent
from models import ChainRow, MarketTick, OptionChain, OptionType


def tick(option_type: OptionType, *, bid: float = 99, ask: float = 100, volume: int = 2_000_000, oi: int = 25_000_000) -> MarketTick:
    suffix = "CE" if option_type is OptionType.CALL else "PE"
    return MarketTick(
        instrument=f"NFO:NIFTY26SEP24800{suffix}",
        index="NIFTY 50",
        strike=24800,
        expiry="2026-09-04",
        option_type=option_type,
        bid=bid,
        ask=ask,
        ltp=99.5,
        oi=oi,
        volume=volume,
        iv=12.5,
        timestamp=datetime.now(timezone.utc),
    )


def test_score_uses_explainable_live_liquidity_components() -> None:
    result = score_tick(tick(OptionType.CALL))

    assert spread_percent(tick(OptionType.CALL)) == 1.0
    assert result.components.spread == 30.0
    assert result.components.volume == 30.0
    assert result.components.open_interest == 30.0
    assert result.score == 90.0


def test_tight_spread_and_higher_liquidity_ranks_first() -> None:
    strong = tick(OptionType.CALL, bid=99, ask=100, volume=2_000_000, oi=25_000_000)
    weak = tick(OptionType.PUT, bid=80, ask=100, volume=100_000, oi=1_000_000)
    chain = OptionChain(index="NIFTY 50", expiry="2026-09-04", rows=[ChainRow(strike=24800, call=strong, put=weak)])

    rankings = rank_option_chain(chain)

    assert [ranking.instrument for ranking in rankings] == [strong.instrument, weak.instrument]


def test_option_type_filter_returns_only_requested_contracts() -> None:
    call = tick(OptionType.CALL)
    put = tick(OptionType.PUT)
    chain = OptionChain(index="NIFTY 50", expiry="2026-09-04", rows=[ChainRow(strike=24800, call=call, put=put)])

    rankings = rank_option_chain(chain, OptionType.PUT)

    assert [ranking.option_type for ranking in rankings] == [OptionType.PUT]
