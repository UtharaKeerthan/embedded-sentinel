"""
safety_agent.py
ISO 26262 ASIL classification agent.
"""
from crewai import Agent, Task
from langchain_community.llms import Ollama

LLM = Ollama(model="codellama:7b")

def build_safety_agent(vectorstore):
    return Agent(
        role="ISO 26262 Functional Safety Engineer",
        goal="Classify each ISP pipeline module by ASIL level and identify safety gaps",
        backstory=("You are a TÜV-certified functional safety engineer specialising "
                   "in automotive software safety per ISO 26262."),
        llm=LLM, verbose=True, allow_delegation=False,
    )

def build_safety_task(agent, repo_path: str):
    return Task(
        description=f"""
Analyse the ISP pipeline modules in {repo_path}/src/ and classify each by ASIL level.

For each module:
1. Identify its role in the image processing chain
2. Assess severity, exposure, and controllability of a failure
3. Assign ASIL-A through ASIL-D (or QM)
4. Note missing safety mechanisms

Output to reports/safety_analysis.md
""",
        agent=agent,
        expected_output="ASIL classification table per module with rationale."
    )
