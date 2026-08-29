from datetime import datetime, timezone

from models import AlertEvent, AlertRule, ContractScore
from store import RuleStore


def matching_contracts(rule: AlertRule, rankings: list[ContractScore]) -> list[ContractScore]:
    matches: list[ContractScore] = []
    for contract in rankings:
        if rule.option_type is not None and contract.option_type is not rule.option_type:
            continue
        if rule.min_score is not None and contract.score < rule.min_score:
            continue
        if rule.max_spread_percent is not None and contract.spread_percent > rule.max_spread_percent:
            continue
        matches.append(contract)
    return matches


def evaluate_rule(rule: AlertRule, rankings: list[ContractScore], store: RuleStore) -> list[AlertEvent]:
    now = datetime.now(timezone.utc)
    events: list[AlertEvent] = []
    for contract in matching_contracts(rule, rankings):
        if store.can_trigger(rule, contract.instrument, now):
            store.mark_triggered(rule, contract.instrument, now)
            events.append(
                AlertEvent(
                    rule_id=rule.id,
                    instrument=contract.instrument,
                    score=contract.score,
                    spread_percent=contract.spread_percent,
                    triggered_at=now,
                )
            )
    return events
