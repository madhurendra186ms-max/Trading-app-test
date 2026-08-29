from collections import defaultdict

from models import ChainRow, MarketTick, OptionChain, OptionType


def build_option_chain(ticks: list[MarketTick], index: str, expiry: str) -> OptionChain:
    pairs: dict[float, dict[OptionType, MarketTick]] = defaultdict(dict)
    for tick in ticks:
        if tick.index == index and tick.expiry == expiry:
            pairs[tick.strike][tick.option_type] = tick

    rows = [
        ChainRow(strike=strike, call=pair.get(OptionType.CALL), put=pair.get(OptionType.PUT))
        for strike, pair in sorted(pairs.items())
    ]
    return OptionChain(index=index, expiry=expiry, rows=rows)


def list_expiries(ticks: list[MarketTick], index: str) -> list[str]:
    return sorted({tick.expiry for tick in ticks if tick.index == index})
