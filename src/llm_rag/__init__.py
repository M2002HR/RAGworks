"""Lightweight keyword-matching RAG components, reusable across projects."""
from .rag_stub import answer
from .index_stub import SimpleIndex
from .pipeline import rag_pipeline, build_index
from .demo_app import create_demo

__all__ = ["answer", "SimpleIndex", "rag_pipeline", "build_index", "create_demo"]
__version__ = "0.5.0"
