"""
misra_agent.py
MISRA C++:2008 compliance checker agent.
"""
from crewai import Agent, Task
from langchain_community.llms import Ollama
from pathlib import Path
import glob

LLM = Ollama(model="codellama:7b")

MISRA_SYSTEM = """You are a MISRA C++:2008 compliance expert.
Given a C++ code snippet and relevant MISRA rules, identify all violations.
For each violation state: file, approximate line, rule ID, severity (Mandatory/Required/Advisory),
and a brief explanation. Output as a markdown table."""

def build_misra_agent(vectorstore):
    return Agent(
        role="MISRA C++ Compliance Auditor",
        goal="Identify all MISRA C++:2008 violations in the codebase",
        backstory=("You have 15 years of experience auditing safety-critical "
                   "automotive C++ code against MISRA standards."),
        llm=LLM,
        verbose=True,
        allow_delegation=False,
    )

def _collect_cpp_files(repo_path: str) -> list:
    patterns = ["**/*.cpp", "**/*.hpp"]
    files = []
    for p in patterns:
        files.extend(glob.glob(str(Path(repo_path) / p), recursive=True))
    return sorted(files)

def build_misra_task(agent, repo_path: str):
    cpp_files = _collect_cpp_files(repo_path)
    file_list = "\n".join(f"  - {f}" for f in cpp_files[:20])

    return Task(
        description=f"""
Scan the embedded-isp-pipeline C++ codebase for MISRA C++:2008 violations.

Files to analyse:
{file_list}

For each file, check for violations including but not limited to:
- Rule 18-4-1: No dynamic memory (malloc, new)
- Rule 15-0-1: No exceptions
- Rule 5-0-8: No precision-reducing casts
- Rule 7-5-4: No recursion
- Rule 6-4-1: All if-else chains have final else

Output your findings to reports/misra_violations.md
""",
        agent=agent,
        expected_output="A markdown report of all MISRA violations with file, rule, severity."
    )
