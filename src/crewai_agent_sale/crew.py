from crewai import Agent, Crew, Process, Task
from crewai.a2a import A2AServerConfig
from crewai.a2a.auth import SimpleTokenAuth
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel

from crewai_agent_sale.fake_llm import llm
from crewai_agent_sale.script import SaleFakeLLM
from crewai_agent_sale.tools.forecast import SalesForecastTool


class SaleForecast(BaseModel):
    policy_version: str
    target_leads: int
    deals: int
    revenue: int
    commission: int
    sales_headcount_needed: int
    sales_headcount_planned: int
    quota_per_rep: int
    capped_by_hr: bool
    risks: list[str] = []
    note: str = ""


@CrewBase
class CrewaiAgentSale():
    """Sale: một agent, gọi được trực tiếp (/kickoff) hoặc qua A2A (AMP mở /a2a; token = AUTH_TOKEN)."""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def sales_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['sales_lead'],  # type: ignore[index]
            tools=[SalesForecastTool()],
            llm=llm(SaleFakeLLM),
            max_iter=4,
            a2a=A2AServerConfig(name="Sale", description="Dự báo doanh số và nhân lực bán hàng cho chiến dịch",
                                auth=SimpleTokenAuth()),
            verbose=True,
        )

    @task
    def forecast_task(self) -> Task:
        return Task(
            config=self.tasks_config['forecast_task'],  # type: ignore[index]
            output_pydantic=SaleForecast,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
