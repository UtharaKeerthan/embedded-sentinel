# embedded-sentinel

A multi-agent AI system built with CrewAI, LangChain, and ChromaDB that autonomously analyses the [embedded-isp-pipeline](https://github.com/UtharaKeerthan/embedded-isp-pipeline) C++ codebase. It checks MISRA C++ compliance, classifies ISO 26262 ASIL safety levels, generates Doxygen documentation, creates unit test skeletons, and produces a full requirements traceability matrix — all without human intervention.

This mirrors the kind of AI-assisted SDLC platform described in NXP's AI Community guidelines: multi-agent orchestration applied to embedded safety-critical software engineering workflows.

---

## What it does

Point EmbedSentinel at the ISP pipeline repository and it runs five specialised agents in sequence:

| Agent | Input | Output |
|---|---|---|
| **MISRA Agent** | All `.cpp` / `.hpp` files | Violations with file, line, rule ID, and severity |
| **Safety Agent** | All `.cpp` / `.hpp` files | ASIL classification per pipeline stage |
| **Doc Agent** | All function signatures | Ready-to-paste Doxygen comments |
| **Test Generator** | Functions with no test coverage | Unit test skeletons with assertions |
| **Traceability Agent** | `@req` + `@tc` annotations in code | Requirements traceability matrix |

Each agent queries its own RAG knowledge base (ChromaDB) to retrieve relevant rules, standards clauses, or documentation conventions before reasoning about the code.

---

## Architecture

```
embedsentinel/
        │
        ▼
  crew.py  (top-level orchestrator)
        │
        ├── misra_agent.py
        │     queries RAG: misra_cpp_rules.md
        │     scans: all .cpp/.hpp files
        │     output: reports/misra_violations.md
        │
        ├── safety_agent.py
        │     queries RAG: iso26262_part6.md
        │     scans: all pipeline stage files
        │     output: reports/safety_analysis.md
        │
        ├── doc_agent.py
        │     queries RAG: doxygen_style.md
        │     scans: all function signatures
        │     output: reports/generated_doxygen.md
        │
        ├── test_generator.py
        │     queries RAG: test_strategy.md
        │     scans: functions without @tc annotations
        │     output: reports/generated_tests.md
        │
        └── traceability_agent.py
              queries RAG: requirements_spec.md
              scans: @req tags in code, @tc tags in tests
              output: reports/traceability_matrix.md
```

### RAG knowledge base

Each agent retrieves domain-specific context from ChromaDB before reasoning. The knowledge base is built once from Markdown documents in `rag/docs/`:

```
rag/docs/
├── misra_cpp_rules.md       MISRA C++:2008 rule summaries (shared)
├── iso26262_part6.md        ISO 26262 Part 6 software requirements (shared)
├── doxygen_style.md         Doxygen documentation conventions (shared)
├── requirements_spec.md     Copy of ISP pipeline SRS.md for agent context
└── test_strategy.md         Testing workflow, coverage targets, naming conventions
```

### How the RAG retrieval works

For each chunk of code the agent analyses, a semantic query is sent to ChromaDB:

```python
# Example: MISRA agent retrieves relevant rules for a code chunk
results = vectorstore.similarity_search(
    query="static array access without bounds check in C++",
    k=5,
    collection_name="misra_knowledge"
)
# Returns the 5 most relevant MISRA rules
# Agent then reasons: "Given this code and these rules, what violations exist?"
```

---

## Folder structure

```
embedsentinel/
│
├── crew.py                         Top-level orchestrator — entry point
│
├── agents/
│   ├── misra_agent.py              Scans .cpp/.hpp for MISRA C++ violations
│   ├── safety_agent.py             Classifies ASIL level per pipeline stage
│   ├── doc_agent.py                Generates Doxygen comments for all functions
│   ├── test_generator.py           Generates unit test skeletons for uncovered functions
│   └── traceability_agent.py       Scans @req + @tc tags → builds traceability matrix
│
├── rag/
│   ├── ingest.py                   Builds ChromaDB vector store from docs/
│   ├── knowledge_base.py           Routes documents to the correct collection
│   └── docs/
│       ├── misra_cpp_rules.md      MISRA C++:2008 rule summaries
│       ├── iso26262_part6.md       ISO 26262 Part 6 software safety requirements
│       ├── doxygen_style.md        Doxygen documentation conventions
│       ├── requirements_spec.md    ISP pipeline SRS.md for agent RAG context
│       └── test_strategy.md        Testing workflow and coverage strategy
│
├── reports/                        Agent output — regenerated on each run
│   ├── misra_violations.md         Violations with file, line, rule ID, severity
│   ├── safety_analysis.md          ASIL classification per module
│   ├── generated_doxygen.md        Ready-to-paste Doxygen comments
│   ├── generated_tests.md          Unit test skeletons for uncovered functions
│   └── traceability_matrix.md      REQ → implementation → test case mapping
│
└── requirements.txt
```

---

## Installation

```bash
git clone https://github.com/yourname/embedsentinel.git
cd embedsentinel
pip install -r requirements.txt
```

**`requirements.txt`**
```
crewai
langchain
langchain-community
chromadb
sentence-transformers
ollama
```

Install Ollama and pull a code-capable model:

```bash
# Install Ollama (https://ollama.com)
ollama pull codellama:7b
```

Or use the free Groq API (no local GPU needed) by setting `GROQ_API_KEY` in your environment.

---

## Usage

### Step 1 — Build the RAG knowledge base (once)

```bash
python rag/ingest.py
# Reads all documents in rag/docs/
# Builds ChromaDB collections: misra_knowledge, safety_knowledge, etc.
```

### Step 2 — Run the full agent crew

```bash
python crew.py --repo ../embedded-isp-pipeline/
```

This runs all five agents in sequence against the ISP pipeline codebase. Reports appear in `reports/`.

### Step 3 — Run a single agent

```bash
# MISRA check only
python crew.py --repo ../embedded-isp-pipeline/ --agent misra

# Traceability matrix only
python crew.py --repo ../embedded-isp-pipeline/ --agent traceability

# Documentation generation only
python crew.py --repo ../embedded-isp-pipeline/ --agent doc
```

---

## Sample outputs

### `reports/misra_violations.md`

```markdown
## MISRA C++ Violations — embedded-isp-pipeline

| File | Line | Rule | Severity | Description |
|---|---|---|---|---|
| src/edge/canny.cpp | 47 | 5-0-8 | Required | Implicit conversion from int32_t to uint8_t may lose data |
| src/color/ccm.cpp | 23 | 18-4-1 | Mandatory | Possible dynamic allocation via std::vector — use static array |
| src/analysis/histogram.cpp | 89 | 7-5-4 | Required | Recursive call detected — MISRA bans recursion |

Total: 3 violations (1 mandatory, 2 required)
```

### `reports/traceability_matrix.md`

```markdown
## Traceability Matrix — embedded-isp-pipeline

| REQ-ID | Description | Implementation File | Test Case IDs | Status |
|---|---|---|---|---|
| REQ-ISP-001 | Demosaic Bayer → RGB | src/core/demosaic.cpp | TC-ISP-001, TC-ISP-002 | ✅ covered |
| REQ-ISP-002 | No dynamic memory | src/core/memory_pool.cpp | TC-MEM-001 | ✅ covered |
| REQ-EDGE-002 | Canny NMS stage | src/edge/canny.cpp | — | ⚠️ untested |
| REQ-AE-001 | Auto-exposure convergence | — | — | ❌ unimplemented |

Coverage: 13 / 15 requirements implemented · 11 / 13 requirements tested
```

### `reports/safety_analysis.md`

```markdown
## ISO 26262 Safety Analysis — embedded-isp-pipeline

| Module | ASIL Classification | Rationale |
|---|---|---|
| src/core/demosaic.cpp | ASIL-B | Output feeds display pipeline; error affects driver perception |
| src/edge/canny.cpp | ASIL-B | Used for lane detection preprocessing in downstream systems |
| src/analysis/auto_exposure.cpp | ASIL-A | Affects image brightness; degraded but not safety-critical alone |
| src/core/memory_pool.cpp | ASIL-D | Allocator failure would crash entire pipeline |
```

---

## Traceability agent — how it works

The traceability agent (`agents/traceability_agent.py`) runs three steps:

**Step 1 — Scan `@req` tags** from all `.cpp` and `.hpp` files in the target repo:
```
src/core/demosaic.cpp   → REQ-ISP-001, REQ-ISP-002, REQ-ISP-003
src/core/white_balance.cpp → REQ-WB-001, REQ-WB-002
...
```

**Step 2 — Scan `@tc` and `@covers` tags** from all test files:
```
tests/unit/test_demosaic.cpp → TC-ISP-001 covers REQ-ISP-001
tests/unit/test_demosaic.cpp → TC-ISP-002 covers REQ-ISP-002
...
```

**Step 3 — Cross-reference** against the SRS loaded from RAG and flag three gap types:

| Gap type | Meaning | Flag |
|---|---|---|
| UNIMPLEMENTED | REQ exists in SRS but no `@req` found in code | ❌ |
| UNTESTED | `@req` in code but no `@tc` covers that REQ | ⚠️ |
| ORPHANED | `@tc` exists but no matching REQ in SRS | 🔵 |

---

## GitHub Actions integration

EmbedSentinel runs automatically on every pull request to the ISP pipeline via a shared workflow. The traceability matrix is posted as a PR comment.

```yaml
# .github/workflows/embedsentinel.yml (in embedded-isp-pipeline repo)
name: EmbedSentinel Analysis
on: [pull_request]

jobs:
  analyse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run EmbedSentinel
        run: |
          git clone https://github.com/yourname/embedsentinel.git ../embedsentinel
          cd ../embedsentinel
          pip install -r requirements.txt
          python rag/ingest.py
          python crew.py --repo ../embedded-isp-pipeline/ --output-format github
      - name: Post traceability matrix as PR comment
        uses: actions/github-script@v6
```

---

## Design decisions

**Why CrewAI?**
CrewAI provides a clean agent-task-crew abstraction that maps well to the multi-agent structure required here. Each agent is a role with a goal, a backstory, and a set of tools. Tasks pass context between agents. The crew orchestrates execution order and inter-agent communication.

**Why ChromaDB?**
ChromaDB is a lightweight, local vector database that runs with no external service. Each agent gets its own named collection, keeping retrieval context isolated. Embeddings are generated locally using `sentence-transformers` — no API key or network access needed.

**Why Ollama + CodeLlama?**
CodeLlama is a code-focused LLM that understands C++ syntax, MISRA patterns, and safety annotation conventions. Ollama runs it locally on CPU, keeping all code and proprietary logic on-premises — matching the data governance approach NXP requires for internal tools.
