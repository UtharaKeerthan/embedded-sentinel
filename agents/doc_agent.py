"""
doc_agent.py
Doxygen documentation generator agent.
"""
from crewai import Agent, Task
from langchain_community.llms import Ollama
import glob
from pathlib import Path

LLM = Ollama(model="codellama:7b")

def build_doc_agent(vectorstore):
    return Agent(
        role="Technical Documentation Specialist",
        goal="Generate complete Doxygen comments for all undocumented functions",
        backstory="Expert in C++ API documentation following automotive documentation standards.",
        llm=LLM, verbose=True, allow_delegation=False,
    )

def build_doc_task(agent, repo_path: str):
    headers = glob.glob(str(Path(repo_path) / "include/**/*.hpp"), recursive=True)
    return Task(
        description=f"""
Scan all header files in {repo_path}/include/ and generate Doxygen comments
for any function that is missing @brief, @param, @return, or @req annotations.

Follow the style guide: brief description, param docs, return value,
and @req tags linking to SRS requirement IDs.

Output ready-to-paste Doxygen comments to reports/generated_doxygen.md
""",
        agent=agent,
        expected_output="Complete Doxygen comment blocks for all undocumented functions."
    )
