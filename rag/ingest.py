"""
ingest.py
Builds ChromaDB vector store collections from all RAG documents.
Run once before using any agents.

Usage:
    python rag/ingest.py
"""
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from knowledge_base import COLLECTION_DOCS, CHROMA_DIR

EMBEDDINGS = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
SPLITTER   = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)

def ingest_collection(name: str, doc_paths: list):
    docs = []
    for path in doc_paths:
        p = Path(path)
        if p.exists():
            text = p.read_text(errors="ignore")
            chunks = SPLITTER.split_text(text)
            from langchain.schema import Document
            docs.extend([Document(page_content=c, metadata={"source": str(p)})
                         for c in chunks])
        else:
            print(f"  [WARN] Missing: {path}")

    if docs:
        Chroma.from_documents(docs, EMBEDDINGS,
                               collection_name=name,
                               persist_directory=str(CHROMA_DIR))
        print(f"  [OK] {name}: {len(docs)} chunks")
    else:
        print(f"  [WARN] {name}: no documents found")

def main():
    CHROMA_DIR.mkdir(exist_ok=True)
    print("Building ChromaDB vector store...")
    for collection_name, paths in COLLECTION_DOCS.items():
        ingest_collection(collection_name, paths)
    print("Done. Run crew.py to start analysis.")

if __name__ == "__main__":
    main()
