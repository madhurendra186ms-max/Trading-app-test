from models import ContractScore, MarketTick, OptionChain, OptionType, ScoreComponents

MAX_VOLUME = 2_000_000
MAX_OPEN_INTEREST = 25_000_000


def spread_percent(tick: MarketTick) -> float:
    if tick.ask == 0:
        return 100.0
    return round((tick.ask - tick.bid) / tick.ask * 100, 4)


def score_tick(tick: MarketTick) -> ContractScore:
    spread = spread_percent(tick)
    components = ScoreComponents(
        spread=round(max(0.0, 40.0 - min(spread, 4.0) * 10.0), 2),
        volume=round(min(tick.volume / MAX_VOLUME * 30.0, 30.0), 2),
        open_interest=round(min(tick.oi / MAX_OPEN_INTEREST * 30.0, 30.0), 2),
    )
    return ContractScore(
        instrument=tick.instrument,
        option_type=tick.option_type,
        strike=tick.strike,
        ltp=tick.ltp,
        spread_percent=spread,
        score=round(components.spread + components.volume + components.open_interest, 2),
        components=components,
    )


def rank_option_chain(chain: OptionChain, option_type: OptionType | None = None) -> list[ContractScore]:
    ticks: list[MarketTick] = []
    for row in chain.rows:
        for tick in (row.call, row.put):
            if tick is not None and (option_type is None or tick.option_type is option_type):
                ticks.append(tick)
    return sorted((score_tick(tick) for tick in ticks), key=lambda result: result.score, reverse=True)
