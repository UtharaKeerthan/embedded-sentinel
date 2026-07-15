"""
test_generator.py
Unit test skeleton generator agent.
"""
from crewai import Agent, Task
from langchain_community.llms import Ollama

LLM = Ollama(model="codellama:7b")

def build_test_gen_agent(vectorstore):
    return Agent(
        role="Embedded Software Test Engineer",
        goal="Generate GoogleTest unit test skeletons for functions lacking @tc coverage",
        backstory="Expert in embedded C++ testing with focus on boundary cases and MISRA-safe test patterns.",
        llm=LLM, verbose=True, allow_delegation=False,
    )

def build_test_gen_task(agent, repo_path: str):
    return Task(
        description=f"""
Cross-reference all function declarations in {repo_path}/include/ against
existing @tc annotations in {repo_path}/tests/.

For each function with no corresponding test case:
1. Generate a GoogleTest TEST() skeleton
2. Include at least: happy path, null input, boundary value tests
3. Add @tc and @covers Doxygen annotations
4. Follow the naming pattern: TEST(ModuleTest, FunctionName_Scenario)

Output to reports/generated_tests.md
""",
        agent=agent,
        expected_output="GoogleTest skeletons for all uncovered functions."
    )
