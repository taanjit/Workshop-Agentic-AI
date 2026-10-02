"""
Acme Corp Internal Knowledge Base Assistant
Module: Knowledge Base Ingestion Pipeline

This module loads corporate markdown documentation, splits them into semantic
chunks with overlap, computes vector embeddings using FastEmbed, and indexes
them into a local, persistent Chroma vector database.
"""

from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from . import config
from .llm import get_embeddings


def load_documents() -> List[Document]:
    """
    Read all markdown files from the configured knowledge base directory.
    Attaches the source filename as metadata for grounding and attribution.
    """
    docs_path = Path(config.DOCS_DIR)
    if not docs_path.exists():
        docs_path.mkdir(parents=True, exist_ok=True)

    documents: List[Document] = []
    for file_path in docs_path.glob("*.md"):
        try:
            content = file_path.read_text(encoding="utf-8")
            documents.append(
                Document(
                    page_content=content,
                    metadata={"source": file_path.name},
                )
            )
        except Exception as e:
            print(f"⚠️ Error reading '{file_path.name}': {e}")

    return documents


def build_index() -> int:
    """
    Split loaded documents into chunks, compute embeddings, and store in Chroma.
    
    Returns:
        Total number of chunks indexed.
    """
    documents = load_documents()
    if not documents:
        print(f"⚠️ No documents found in '{config.DOCS_DIR}'. Knowledge base is empty.")
        return 0

    # Chunking Strategy:
    # 500 characters balances atomic semantic focus with sufficient context.
    # 80 characters overlap ensures sentences split across boundaries are not lost.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    # Initialize Chroma persistent vector database using local FastEmbed embeddings
    embeddings = get_embeddings()
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=config.CHROMA_DIR,
    )

    return len(chunks)


if __name__ == "__main__":
    print(f"Ingesting documents from '{config.DOCS_DIR}'...")
    count = build_index()
    print(f"✅ Successfully indexed {count} document chunks into '{config.CHROMA_DIR}'.")
