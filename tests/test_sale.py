"""Offline tests: the numbers come from policy.yaml, and the crew finishes its ReAct loop with the scripted LLM."""
import json

from crewai_agent_sale.crew import CrewaiAgentSale, SaleForecast
from crewai_agent_sale.tools.forecast import forecast, policy


def test_forecast_follows_policy():
    p = policy()
    f = forecast(1512)
    assert f["deals"] == round(1512 * p["conversion_rate_pct"] / 100)
    assert f["revenue"] == round(f["deals"] * p["price_per_deal"] * (100 - p["promo_discount_pct"]) / 100)
    assert f["sales_headcount_planned"] == f["sales_headcount_needed"]


def test_forecast_capped_by_hr():
    f = forecast(1512, max_headcount=2)
    assert f["capped_by_hr"] and f["sales_headcount_planned"] == 2 and f["quota_per_rep"] * 2 >= f["deals"]


def test_crew_runs_end_to_end_with_fake_llm(monkeypatch):
    monkeypatch.delenv("MODEL", raising=False)
    monkeypatch.setenv("FAKE_LLM_DELAY", "0")
    out = CrewaiAgentSale().crew().kickoff(inputs={"proposal": json.dumps({"target_leads": 1000})})
    result = SaleForecast.model_validate(out.pydantic.model_dump() if out.pydantic else json.loads(out.raw))
    assert result.target_leads == 1000 and result.deals == forecast(1000)["deals"]
