"""
crew.py - EmbedSentinel top-level orchestrator.
Runs all agents against the embedded-isp-pipeline C++ codebase.

Usage:
    python crew.py --repo ../embedded-isp-pipeline/
    python crew.py --repo ../embedded-isp-pipeline/ --agent misra
"""
import argparse
import os
from pathlib import Path
from crewai import Crew, Process
from agents.misra_agent        import build_misra_agent,       build_misra_task
from agents.safety_agent       import build_safety_agent,      build_safety_task
from agents.doc_agent          import build_doc_agent,         build_doc_task
from agents.test_generator     import build_test_gen_agent,    build_test_gen_task
from agents.traceability_agent import build_traceability_agent, build_traceability_task
from rag.knowledge_base        import get_vectorstore

AGENT_MAP = {
    "misra":         (build_misra_agent,         build_misra_task),
    "safety":        (build_safety_agent,         build_safety_task),
    "doc":           (build_doc_agent,            build_doc_task),
    "test":          (build_test_gen_agent,       build_test_gen_task),
    "traceability":  (build_traceability_agent,   build_traceability_task),
}

def run(repo_path: str, agent_name: str = "all"):
    repo = Path(repo_path).resolve()
    if not repo.exists():
        raise FileNotFoundError(f"Repo not found: {repo}")

    vs = get_vectorstore()

    if agent_name != "all" and agent_name in AGENT_MAP:
        agent_fn, task_fn = AGENT_MAP[agent_name]
        agent  = agent_fn(vs)
        task   = task_fn(agent, str(repo))
        crew   = Crew(agents=[agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        print(result)
        return

    # Full crew
    agents = [fn(vs) for fn, _ in AGENT_MAP.values()]
    tasks  = [task_fn(agent_fn(vs), str(repo))
              for (agent_fn, task_fn) in AGENT_MAP.values()]
    crew   = Crew(agents=agents, tasks=tasks,
                  process=Process.sequential, verbose=True)
    result = crew.kickoff()
    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EmbedSentinel ISP analyser")
    parser.add_argument("--repo",  required=True, help="Path to embedded-isp-pipeline repo")
    parser.add_argument("--agent", default="all",
                        choices=list(AGENT_MAP.keys()) + ["all"])
    args = parser.parse_args()
    run(args.repo, args.agent)
