"""What the scripted model says as the Sale lead (see fake_llm.py)."""
from __future__ import annotations

from crewai_agent_sale.fake_llm import ScriptedLLM, act, final, first_json, last_observation


class SaleFakeLLM(ScriptedLLM):
    def respond(self, text: str) -> str:
        obs = last_observation(text)
        if obs is None:
            req = first_json(text)
            args = {"target_leads": int(req.get("target_leads", 1000))}
            if req.get("max_headcount"):
                args["max_headcount"] = int(req["max_headcount"])
            return act("sales_forecast", args, "Cần số liệu dự báo theo chính sách bán hàng trước khi trả lời.")
        risks = []
        if obs["capped_by_hr"]:
            risks.append(f"HR chỉ đáp ứng {obs['sales_headcount_planned']} người: chỉ tiêu tăng lên "
                         f"{obs['quota_per_rep']} hợp đồng/người/quý")
        if obs["promo_discount_pct"] >= 15:
            risks.append("khuyến mãi sâu làm giảm biên lợi nhuận")
        revenue = f"{obs['revenue']:,}đ".replace(",", ".")
        note = (f"Với {obs['target_leads']} lead, dự kiến {obs['deals']} hợp đồng, doanh số sau khuyến mãi {revenue} "
                f"(chính sách {obs['policy_version']}); cần {obs['sales_headcount_planned']} nhân viên bán hàng, "
                f"chỉ tiêu {obs['quota_per_rep']} hợp đồng/người.")
        return final({**obs, "risks": risks, "note": note}, "Đã có số liệu, tổng hợp cho Marketing.")
