from datetime import datetime, timezone

import httpx
import pytest

from engine import evaluate_rule, matching_contracts
from main import app
from models import AlertRule, ContractScore, OptionType
from store import RuleStore


def contract(option_type: OptionType, score: float, spread_percent: float) -> ContractScore:
    suffix = "CE" if option_type is OptionType.CALL else "PE"
    return ContractScore(
        instrument=f"NFO:NIFTY26SEP24800{suffix}",
        option_type=option_type,
        strike=24800,
        ltp=100,
        score=score,
        spread_percent=spread_percent,
    )


def rule(**changes: object) -> AlertRule:
    defaults: dict[str, object] = {
        "index": "NIFTY 50",
        "expiry": "2026-09-04",
        "min_score": 90,
        "max_spread_percent": 1,
        "cooldown_seconds": 60,
    }
    defaults.update(changes)
    return AlertRule.model_validate(defaults)


def test_matching_contracts_applies_score_spread_and_option_type() -> None:
    matching = contract(OptionType.CALL, 95, 0.5)
    wrong_type = contract(OptionType.PUT, 95, 0.5)
    poor_score = contract(OptionType.CALL, 80, 0.5)

    matches = matching_contracts(rule(option_type=OptionType.CALL), [matching, wrong_type, poor_score])

    assert matches == [matching]


def test_evaluation_respects_the_per_instrument_cooldown() -> None:
    alert_rule = rule()
    store = RuleStore()
    rankings = [contract(OptionType.CALL, 95, 0.5)]

    first_events = evaluate_rule(alert_rule, rankings, store)
    second_events = evaluate_rule(alert_rule, rankings, store)

    assert len(first_events) == 1
    assert second_events == []


def test_zero_cooldown_allows_each_evaluation() -> None:
    alert_rule = rule(cooldown_seconds=0)
    store = RuleStore()
    rankings = [contract(OptionType.CALL, 95, 0.5)]

    assert len(evaluate_rule(alert_rule, rankings, store)) == 1
    assert len(evaluate_rule(alert_rule, rankings, store)) == 1


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_create_rule_returns_a_generated_identifier() -> None:
    app.state.rule_store = RuleStore()
    transport = httpx.ASGITransport(app=app)
    payload = {
        "index": "NIFTY 50",
        "expiry": "2026-09-04",
        "option_type": "CE",
        "min_score": 90,
    }
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/v1/rules", json=payload)

    assert response.status_code == 201
    assert response.json()["id"]
