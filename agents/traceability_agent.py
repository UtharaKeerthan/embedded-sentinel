"""
traceability_agent.py
Requirements traceability agent.
Scans @req and @tc annotations. Generates the traceability matrix.
"""
import re
import glob
from pathlib import Path
from crewai import Agent, Task
from langchain_community.llms import Ollama

LLM = Ollama(model="codellama:7b")

def build_traceability_agent(vectorstore):
    return Agent(
        role="Requirements Traceability Engineer",
        goal="Produce a complete traceability matrix linking requirements to implementation to tests",
        backstory="Expert in ASPICE SWE.5/SWE.6 traceability for automotive software.",
        llm=LLM, verbose=True, allow_delegation=False,
    )

def scan_req_tags(repo_path: str) -> dict:
    """Returns {REQ-ID: [file_paths]} from @req annotations in source."""
    req_map: dict = {}
    for f in glob.glob(str(Path(repo_path) / "**/*.cpp"), recursive=True) +              glob.glob(str(Path(repo_path) / "**/*.hpp"), recursive=True):
        content = Path(f).read_text(errors="ignore")
        for req_id in re.findall(r"@req\s+(REQ-[\w-]+)", content):
            req_map.setdefault(req_id, []).append(f)
    return req_map

def scan_tc_tags(repo_path: str) -> dict:
    """Returns {TC-ID: {covers: [REQ-IDs], file: path}} from @tc annotations in tests."""
    tc_map: dict = {}
    for f in glob.glob(str(Path(repo_path) / "tests/**/*.cpp"), recursive=True):
        content = Path(f).read_text(errors="ignore")
        tc_ids  = re.findall(r"@tc\s+(TC-[\w-]+)", content)
        covers  = re.findall(r"@covers\s+(REQ-[\w-]+)", content)
        for tc_id in tc_ids:
            tc_map[tc_id] = {"covers": covers, "file": f}
    return tc_map

def build_traceability_task(agent, repo_path: str):
    req_map = scan_req_tags(repo_path)
    tc_map  = scan_tc_tags(repo_path)

    return Task(
        description=f"""
Build the traceability matrix for {repo_path}.

Found @req annotations: {list(req_map.keys())}
Found @tc  annotations: {list(tc_map.keys())}

Cross-reference against requirements/SRS.md to find:
- UNIMPLEMENTED: REQ in SRS but no @req in code
- UNTESTED: @req in code but no @tc covers it
- ORPHANED: @tc exists but no matching REQ in SRS

Write the matrix to reports/traceability_matrix.md and also copy it to
{repo_path}/requirements/traceability_matrix.md
""",
        agent=agent,
        expected_output="Markdown traceability matrix with coverage percentage."
    )
