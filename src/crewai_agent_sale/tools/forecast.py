"""sales_forecast: the numbers come from code and policy.yaml, never from the model."""
from __future__ import annotations

import json
import math
from pathlib import Path

import yaml
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

POLICY = Path(__file__).resolve().parents[1] / "policy.yaml"


def policy() -> dict:
    return yaml.safe_load(POLICY.read_text())


def forecast(target_leads: int, max_headcount: int | None = None) -> dict:
    p = policy()
    deals = round(target_leads * p["conversion_rate_pct"] / 100)
    gross = deals * p["price_per_deal"]
    revenue = round(gross * (100 - p["promo_discount_pct"]) / 100)
    needed = max(1, math.ceil(deals / p["deals_per_rep_per_quarter"]))
    reps = min(needed, max_headcount) if max_headcount else needed
    return {"policy_version": p["version"], "target_leads": target_leads, "deals": deals,
            "revenue_before_promo": gross, "promo_discount_pct": p["promo_discount_pct"], "revenue": revenue,
            "commission": round(revenue * p["commission_pct"] / 100), "sales_headcount_needed": needed,
            "sales_headcount_planned": reps, "quota_per_rep": math.ceil(deals / reps),
            "capped_by_hr": bool(max_headcount and needed > max_headcount)}


class ForecastInput(BaseModel):
    target_leads: int = Field(..., description="Số lead chiến dịch dự kiến mang về")
    max_headcount: int | None = Field(None, description="Số nhân viên bán hàng tối đa HR đáp ứng được (nếu có)")


class SalesForecastTool(BaseTool):
    name: str = "sales_forecast"
    description: str = ("Tính dự báo doanh số, hoa hồng, số nhân viên bán hàng cần và chỉ tiêu mỗi người từ số lead, "
                        "theo chính sách bán hàng hiện hành. Trả JSON.")
    args_schema: type[BaseModel] = ForecastInput

    def _run(self, target_leads: int, max_headcount: int | None = None) -> str:
        return json.dumps(forecast(int(target_leads), max_headcount), ensure_ascii=False)
