"""Lightweight keyword-matching RAG components, reusable across projects."""
from .rag_stub import answer
from .index_stub import SimpleIndex

__all__ = ["answer", "SimpleIndex"]
__version__ = "0.2.0"
