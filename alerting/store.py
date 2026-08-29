from datetime import datetime

from models import AlertRule


class RuleStore:
    def __init__(self) -> None:
        self._rules: dict[str, AlertRule] = {}
        self._last_triggered: dict[tuple[str, str], datetime] = {}

    def add(self, rule: AlertRule) -> AlertRule:
        self._rules[rule.id] = rule
        return rule

    def list(self) -> list[AlertRule]:
        return list(self._rules.values())

    def can_trigger(self, rule: AlertRule, instrument: str, now: datetime) -> bool:
        previous = self._last_triggered.get((rule.id, instrument))
        return previous is None or (now - previous).total_seconds() >= rule.cooldown_seconds

    def mark_triggered(self, rule: AlertRule, instrument: str, now: datetime) -> None:
        self._last_triggered[(rule.id, instrument)] = now
