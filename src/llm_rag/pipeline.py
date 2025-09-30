"""Reusable RAG pipeline utilities (no external LLM calls)."""
from __future__ import annotations
from typing import Sequence, Mapping, Union, Optional
from .index_stub import SimpleIndex
from .rag_stub import answer as _answer

Doc = Union[str, Mapping]

def build_index(docs: Sequence[Doc]) -> SimpleIndex:
    """Build and return a SimpleIndex over the given docs."""
    idx = SimpleIndex()
    idx.add_many(docs)
    return idx

def rag_pipeline(query: str, *, docs: Optional[Sequence[Doc]] = None, index: Optional[SimpleIndex] = None, k: int = 3) -> str:
    """Search docs via SimpleIndex then produce a stub answer.

    Provide either `docs` (we'll build an index) or an existing `index`.
    """
    if index is None:
        if docs is None:
            raise ValueError("Provide `docs` or `index`.")
        index = build_index(docs)
    hits = index.search(query, k=k)
    top_texts = [h["text"] for h in hits]
    return _answer(query, top_texts)
