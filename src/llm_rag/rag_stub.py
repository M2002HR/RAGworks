"""Keyword-matching RAG stub (no external dependencies, no API keys required).

This module provides `answer(query, docs)` which picks the best-matching document
via simple keyword overlap and returns a short stub 'answer' string. It is
intentionally minimal and reusable.
"""
from typing import Sequence, Mapping, Union
import re

Doc = Union[str, Mapping]

_WORD_RE = re.compile(r"[A-Za-z0-9]+")

def _tokenise(text: str) -> set[str]:
    return set(_WORD_RE.findall(text.lower()))

def _to_text(doc: Doc) -> str:
    if isinstance(doc, str):
        return doc
    if isinstance(doc, Mapping):
        return str(doc.get("text", ""))
    return str(doc)

def answer(query: str, docs: Sequence[Doc]) -> str:
    """Return a stub RAG-like answer based on simple keyword overlap.

    Args:
        query: The user question.
        docs: Sequence of documents (strings or mappings with a 'text' key).

    Returns:
        A short string containing a stub 'answer' derived from the best-matching document.
    """
    if not docs:
        return "No documents provided. (stub RAG)"

    q_tokens = _tokenise(query)
    best_idx = 0
    best_score = -1
    best_text = ""

    for i, d in enumerate(docs):
        text = _to_text(d)
        t_tokens = _tokenise(text)
        score = len(q_tokens & t_tokens)
        if score > best_score:
            best_score = score
            best_idx = i
            best_text = text

    if best_score <= 0:
        best_text = _to_text(docs[0])

    snippet = best_text.strip().replace("\n", " ")
    if len(snippet) > 160:
        snippet = snippet[:157] + "..."
    return f"Answer (stub): {snippet}"
