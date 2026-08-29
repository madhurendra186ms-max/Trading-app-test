import httpx
from fastapi import APIRouter, FastAPI, HTTPException, Request, status

from client import fetch_rankings
from engine import evaluate_rule
from models import AlertRule, AlertRuleCreate, EvaluationResult, ServiceHealth
from store import RuleStore

app = FastAPI(title="alerting", version="0.1.0")
app.state.rule_store = RuleStore()
router = APIRouter(prefix="/v1", tags=["session alerts"])


@app.get("/health", response_model=ServiceHealth, tags=["operations"])
def health() -> ServiceHealth:
    return ServiceHealth(service="alerting")


@router.post("/rules", response_model=AlertRule, status_code=status.HTTP_201_CREATED)
def create_rule(rule_input: AlertRuleCreate, request: Request) -> AlertRule:
    return request.app.state.rule_store.add(AlertRule(**rule_input.model_dump()))


@router.get("/rules", response_model=list[AlertRule])
def list_rules(request: Request) -> list[AlertRule]:
    return request.app.state.rule_store.list()


@router.post("/evaluate", response_model=EvaluationResult)
async def evaluate_rules(request: Request) -> EvaluationResult:
    store = request.app.state.rule_store
    events = []
    for rule in store.list():
        try:
            rankings = await fetch_rankings(rule.index, rule.expiry)
        except httpx.HTTPError as error:
            raise HTTPException(status_code=503, detail="Scoring service is unavailable") from error
        events.extend(evaluate_rule(rule, rankings.rankings, store))
    return EvaluationResult(triggered=events)


app.include_router(router)
