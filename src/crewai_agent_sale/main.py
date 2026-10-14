#!/usr/bin/env python
import json
import sys

from crewai_agent_sale.crew import CrewaiAgentSale

SAMPLE = {"proposal": json.dumps({"campaign": "Tori Insight Q1/2027", "target_leads": 1512,
                                  "budget": 300000000}, ensure_ascii=False)}


def run():
    result = CrewaiAgentSale().crew().kickoff(inputs=SAMPLE)
    print(result.raw)


def run_with_trigger():
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")
    payload = json.loads(sys.argv[1])
    proposal = payload.get("proposal", payload)
    inputs = {"proposal": proposal if isinstance(proposal, str) else json.dumps(proposal, ensure_ascii=False)}
    return CrewaiAgentSale().crew().kickoff(inputs=inputs)


def train():
    CrewaiAgentSale().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=SAMPLE)


def replay():
    CrewaiAgentSale().crew().replay(task_id=sys.argv[1])


def test():
    CrewaiAgentSale().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=SAMPLE)


if __name__ == "__main__":
    run()
