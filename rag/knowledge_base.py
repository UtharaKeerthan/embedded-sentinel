"""
knowledge_base.py
Defines which documents go into which ChromaDB collection.
"""
from pathlib import Path
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DOCS_DIR   = Path(__file__).parent / "docs"
CHROMA_DIR = Path(__file__).parent / ".chromadb"

COLLECTION_DOCS = {
    "misra_knowledge": [
        DOCS_DIR / "misra_cpp_rules.md",
        DOCS_DIR / "doxygen_style.md",
    ],
    "safety_knowledge": [
        DOCS_DIR / "iso26262_part6.md",
        DOCS_DIR / "misra_cpp_rules.md",
    ],
    "requirements_knowledge": [
        DOCS_DIR / "requirements_spec.md",
        DOCS_DIR / "test_strategy.md",
    ],
    "doc_knowledge": [
        DOCS_DIR / "doxygen_style.md",
    ],
}

_vectorstores: dict = {}

def get_vectorstore(collection: str = "misra_knowledge") -> Chroma:
    if collection not in _vectorstores:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        _vectorstores[collection] = Chroma(
            collection_name=collection,
            embedding_function=embeddings,
            persist_directory=str(CHROMA_DIR),
        )
    return _vectorstores[collection]
