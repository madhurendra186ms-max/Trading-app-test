from collections.abc import Iterable

from models import MarketTick


class TickStore:
    def __init__(self) -> None:
        self._ticks: dict[str, MarketTick] = {}

    def upsert(self, tick: MarketTick) -> MarketTick:
        current = self._ticks.get(tick.instrument)
        if current is None or tick.timestamp >= current.timestamp:
            self._ticks[tick.instrument] = tick
        return self._ticks[tick.instrument]

    def get(self, instrument: str) -> MarketTick | None:
        return self._ticks.get(instrument)

    def list(self) -> Iterable[MarketTick]:
        return sorted(self._ticks.values(), key=lambda tick: tick.instrument)

    def count(self) -> int:
        return len(self._ticks)

    def top_indexes_by_volume(self, limit: int) -> list[tuple[str, int]]:
        totals: dict[str, int] = {}
        for tick in self._ticks.values():
            totals[tick.index] = totals.get(tick.index, 0) + tick.volume
        return sorted(totals.items(), key=lambda item: item[1], reverse=True)[:limit]
