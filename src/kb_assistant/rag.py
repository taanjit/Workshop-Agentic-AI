"""
Acme Corp Internal Knowledge Base Assistant
Module: Vector Retrieval Pipeline (RAG Engine)

This module interfaces with the persistent Chroma vector store to perform
k-Nearest Neighbor (k-NN) similarity searches based on semantic embeddings.
"""

from typing import List, Dict, Any, Optional
from langchain_chroma import Chroma
from . import config
from .llm import get_embeddings

# Singleton instance to prevent redundant database connection overhead
_vector_store: Optional[Chroma] = None


def _get_store() -> Chroma:
    """Initialize or return the cached Chroma vector store instance."""
    global _vector_store
    if _vector_store is None:
        _vector_store = Chroma(
            persist_directory=config.CHROMA_DIR,
            embedding_function=get_embeddings(),
        )
    return _vector_store


def retrieve(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """
    Retrieve the top-k most semantically relevant document chunks for a query.
    
    Args:
        query: The user's question or search phrase.
        k: Maximum number of chunks to return (default: 3).
        
    Returns:
        List of dictionaries containing 'text' and 'source' metadata.
    """
    store = _get_store()
    try:
        # Perform cosine similarity search in embedded vector space
        results = store.similarity_search(query, k=k)
        return [
            {
                "text": doc.page_content,
                "source": doc.metadata.get("source", "knowledge_base"),
            }
            for doc in results
        ]
    except Exception as e:
        print(f"⚠️ Vector retrieval error: {e}")
        return []
